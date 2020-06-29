from flask import Flask, Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app
import sys
sys.path.append('/home/pi/smoke/module')
import dbModule

app = Flask(__name__)

@app.route('/show')
def select():
    db_class = dbModule.Database()
    sql = "SELECT * FROM detection"
    row = db_class.executeAll(sql)
    return render_template('showitem.html', items = row)

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['id']
        passw = request.form['pw']       
        if request.method == 'POST':
            db_class = dbModule.Database()
            sql1="SELECT user_id,password From user"
            row1 = db_class.executeAll(sql1)
            for rows1 in row1:
                if rows1['user_id'] == name and rows1['password'] == passw:
                  return redirect(url_for('select'))
            return render_template('login.html')
            
    
    
