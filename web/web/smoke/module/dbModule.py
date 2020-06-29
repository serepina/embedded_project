import pymysql
 
class Database():
    def __init__(self):
        self.db = pymysql.connect(host='detect-db.ccoslhrythv8.ap-northeast-2.rds.amazonaws.com', port=3306, user='admin', passwd='hyejin1234', db='detect_db',charset='utf8',autocommit=True)
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
 
    def execute(self, query, args={}):
        self.cursor.execute(query, args)  
 
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row
 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        print(row)
        return row
 
    def commit():
        self.db.commit()