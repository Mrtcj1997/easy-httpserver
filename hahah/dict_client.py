from socket import *
import sys
import getpass


#创建网络连接
def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    host = sys.argv[1]
    post = int(sys.argv[2])
    s = socket()
    try:
        s.connect((host,post))
    except Exception as e:
        print(e)
        return

    while True:
        print('''
            =========welcome to dict=========
            --1.注册　　　　　2.登录     3.退出
            =================================
            ''')
        cmd = input("输入选项>>")
        if cmd not in ['1','2','3']:
            print("请输入正确选项")
            sys.stdin.flush() #标准输入清楚
            continue
        elif cmd == '1':
            r = do_register(s)
            if r == 1:
                print('用户存在')
            elif r == 2:
                print('注册失败')
            else:
                print('注册成功')
                login(s,r)

        elif cmd == '2':
            name = do_login(s)
            if name:
                print('登录成功')
                login(s,name)
            else:
                print('用户名或密码不正确')

        elif cmd == '3':
            s.send('E'.encode())
            sys.exit(0)

def do_register(s):
    while True:
        a = input('请输入你的用户名:')
        b = getpass.getpass('请输入你的密码:')
        c = getpass.getpass('请再次输入你的密码:')
        if (' ' in a) or (' ' in b):
            print('not space!!!!')
            continue
        if b != c:
            print("zhe passwd don't simple")
            continue
        data = 'R %s#%s'%(a,b)
        s.send(data.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            return a 
        elif data == 'EXISTS':
            return 1
        else :
            return 2 
def do_login(s):
    while True:
        a = input('请输入你的用户名:')
        b = getpass.getpass('请输入你的密码:')
        if (' ' in a) or (' ' in b):
            print('not space!!!!')
            continue
        data = 'L %s#%s'%(a,b)
        s.send(data.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            return a 
        else :
            return
def login(s,name):
    while True:
        print('''=========查询界面=========
                1.查询　  2.历史记录　　　3.退出
                　=========================
                        ''')
        cmd = input("输入选项>>")
        if cmd not in ['1','2','3']:
            print("请输入正确选项")
            sys.stdin.flush() #标准输入清楚
            continue
        elif cmd == '1':
            do_query(s,name)
        elif cmd == '2':
            do_hist(s,name)
        elif cmd == '3':
            return

def do_query(s,name):
    while True:
        word = input('单词>>')
        if word == '##':
            break
        msg ="Q %s#%s"%(name,word)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == 'OK':
            data = s.recv(1024).decode()
            print(data)
        elif data == 'fail':
            print('请输入正确的单词')

def do_hist(s,name):
    msg ="H %s"%name
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print('没有历史记录')

        




if __name__ == '__main__':
    main()

































