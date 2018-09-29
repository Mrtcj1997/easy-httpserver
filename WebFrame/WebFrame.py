#coding = utf - 8
from socket import * 
from setting import *
import time

class Application(object):
    def __init__(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(frame_addr)


    def start(self):
        self.sockfd.listen(5)
        while True:
            c, addr = self.sockfd.accept()
            #接受请求方法
            method = c.recv(128).decode()
            #接受请求内容
            path = c.recv(128).decode()
            print(method,path)
            if method == 'GET':
                if path =='/' or path[-5:] == '.html':
                    status,response_body = self.get_html(path)
                else:
                    response = self.get_data(path)
                #讲结果给httpserver
                c.send(status.encode())
                time.sleep(0.1)
                c.send(response_body.encode())
            elif method == 'POST':
                pass
    
    def get_html(self,path):
        if path == '/':
            get_file = STATIC_DIR + '/index.html'
        else:
            get_file = STATIC_DIR +path
        try:
            f = open(get_file)
        except IOError:
            response = ('404', '=== Sorry not found the page ===')
        else:
            response = ('200',f.read())
        finally:
            return response
    def get_data(self,path):
        pass 

if __name__ == '__main__':
    app = Application()
    app.start()#启动框架等待request