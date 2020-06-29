#!/usr/bin/python
# -*- coding:utf-8 -*-
import pymysql
import boto3
import numpy as np 
import cv2
from PIL import Image
import datetime
import serial
port = '/dev/ttyACM0'
brate = 9600 #boudrate
cmd = 'temp'
seri = serial.Serial(port, baudrate = brate, timeout = None)
print(seri.name)
seri.write(cmd.encode())
s3_resource = boto3.resource(
    's3',
    aws_access_key_id='AKIAJYSIDQ4EEW2TAIDQ',
    aws_secret_access_key='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',
    region_name='ap-northeast-2',
)bucket_name = 'detect-storage'
# Open database connection
db = pymysql.connect(host='detect-db.ccoslhrythv8.ap-northeast-2.rds.amazonaws.com', port=3306, user='admin', passwd='hyejin1234', db='detect_db',charset='utf8',autocommit=True)
# prepare a cursor object using cursor() method
cursor = db.cursor(pymysql.cursors.DictCursor)
def mysql_insert():
    global s3_resource, bucket_name, db, cursor
    # execute SQL query using execute() method.
    sql = "insert into detection(detectday,detecttime,detectposition,detectimage) values (CURDATE(), CURTIME(), %s, %s)"
    address = '부산광역시 부산진구 엄광로 176 정보공학관'
    
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y%m%d%H%M%S')
    print(nowDatetime)  # 2018-07-28 12:11:32
    
    # get image file
    data = open('test.jpg', 'rb')
    
    s_key = nowDatetime+'.jpeg'
    # save image to S3 bucket as public
    s3_resource.Bucket(bucket_name).put_object(Body=data, Key=s_key, ACL='public-read')
    # get public image url
    url = "https://s3-%s.amazonaws.com/%s/%s" % ('ap-northeast-2', bucket_name, s_key)
    cursor.execute(sql, (address, url))
    db.commit()
def inside(r, q): 
    rx, ry, rw, rh = r 
    qx, qy, qw, qh = q 
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh 
def draw_detections(img, rects, thickness = 1): 
    for x, y, w, h in rects: 
     # the HOG detector returns slightly larger rectangles than the real objects. 
     # so we slightly shrink the rectangles to get a nicer output. 
     pad_w, pad_h = int(0.15*w), int(0.05*h) 
     cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness) 
if __name__ == '__main__':
    hog = cv2.HOGDescriptor() 
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) 
    cap=cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    count = 0
    
    found = np.array([])
    while True:
        s,frame=cap.read()
        found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
        draw_detections(frame,found)
        
        if seri.in_waiting != 0 :
            content = seri.readline()
            sensor_list = content.decode()[:len(content)-1]
            print(sensor_list)
            sensor_list.encode("utf-8")
            s = sensor_list.split(',')
        
            if ((type(found) is not tuple and int(s[0]) > 50) and int(s[1]) > 50):
                c = count
                while True:
                    s,frame=cap.read()
                    if (count == (c + fps*30*6)):
                        print("break")
                        break
                    if (((count - c) % (fps*30)) == 0):
                        cv2.imwrite('test.jpg',frame)
                        print("insert")
                        mysql_insert()
                    count += 1
        
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
        count += 1
    cap.release()
    cv2.destroyAllWindows()