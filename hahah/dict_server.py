'''
name : TCJ
data : 2018-10-1
email:996568646@qq.com
modules pymysql
This is a dict
'''

from socket import *
import os 
import time
import signal
import sys
import pymysql

#定义需要的全局变量
DICT_TEXT = './dict.txt'
host = '0.0.0.0'
port = 8888
ADDR = (host,port)

#流程控制
def main():
    #创建数据库连接
    db = pymysql.connect('localhost','root','123456','dict1')

    #创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    #忽略子进程退出
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            c,addr = s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            s.close()
            do_child(c,db)
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        #创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            do_child(c,db)
            sys.exit()
        else:
            c.close()
            continue

def do_child(c,db):
    while True:
        data = c.recv(1024)
        data = data.decode()
        data = data.split(' ')
        l = ' '.join(data[1:])
        if data[0] == 'L':
            do_login(l,db,c)
        elif data[0] == 'R':
            do_register(l,db,c)
        elif  (not data) or data[0] == 'E':
            c.close()
            sys.exit(0)
        elif data[0] == 'Q':
            do_query(c,l,db)
        elif data[0] == 'H':
            do_hist(c,l,db)

def do_hist(c,l,db):
    name = str(l)
    cursor = db.cursor()
    sql = "select * from hist where name = '%s'"%name
    cursor.execute(sql)
    r = cursor.fetchall()
    if not r:
        c.send(b'fail')
        return
    else:
        c.send(b'OK')
    for i in r:
        time.sleep(0.1)
        msg = "%s  %s  %s"%(i[0],i[1],i[2])
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')
def do_query(c,l,db):
    while True:
        l=l.split('#')    
        name = l[0]
        word = l[1]
        cursor = db.cursor()

        def insert_history():
            tm = time.ctime()
            sql = "insert into hist (name,word,time)\
            values('%s','%s','%s')" %(name,word,tm)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
        try:
            f = open(DICT_TEXT)
        except:
            c.send(b'fail')
            return
        for line in f:
            tmp = line.split(' ')[0]
            if tmp >word:
                c.send(b'fail')
                f.close()
                return
            elif tmp == word:
                c.send(b'OK')
                time.sleep(0.1)
                c.send(line.encode())
                f.close()
                insert_history()
                return
        c.send(b'fail')
        f.close()







def do_login(l,db,c):
    l = l.split('#')
    name = l[0]
    passwd = l[1]
    cursor = db.cursor()
    sql = "select name,passwd from user where name = '%s' and passwd = '%s'" % (name,passwd)    
    cursor.execute(sql)
    D=cursor.fetchone()
    print(D)
    if D != None:
        c.send('OK'.encode())
    else:
        c.send('fail'.encode())

def do_register(l,db,c):
    l = l.split('#')
    name = l[0]
    passwd = l[1]
    cursor = db.cursor()
    sql = "select * from user where name = '%s'" % name
    cursor.execute(sql)
    D=cursor.fetchone()
    if D:
        c.send(b'EXISTS')
        return
    sql = "insert into user(name,passwd) values('%s','%s')" % (name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send('OK'.encode())
    except:
        db.rollback()
        c.send('fall'.encode())
    else:
        print('%s注册成功' %name)



if __name__ == '__main__':
    main()




































    



















































