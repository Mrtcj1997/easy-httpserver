import pymysql

def load(s,y)
    db = pymysql.connect('localhost','root','123456','dict1')
    cursor = db.cursor()
    sql = "select name from user where name is '%s'" % s
    cursor.execute(sql)
    D=cursor.fetchone()
    db.commit()
    if d:
        do_load(d)
    elif not d:
        do_reload()

def regi(s,y)
    db = pymysql.connect('localhost','root','123456','dict1')
    cursor = db.cursor()
    sql = "select name from user where name is '%s'" % s
    cursor.execute(sql)
    db.commit()
    if sql:
        do_regi()
    elif  not sql:
        do_reload()

def do_load(d):


