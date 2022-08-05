import queue
import time
from multiprocessing import Process

import requests


class MyProcess(Process):  # 继承Process类
    def __init__(self, name, url):
        super(MyProcess, self).__init__()
        self.name = name
        self.url = url

    def run(self):
        res = requests.get(self.url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})
        q_req_res.put(res)

    def __del__(self):
        del self.name


if __name__ == '__main__':
    q_req_res = queue.Queue()

    p = MyProcess("reqBK", "https://www.baidu.com")
    p.start()
    p.join()
    MyProcess("reqPics").start()

    process_list = []
    for i in range(5):  # 开启5个子进程执行fun1函数
        p = MyProcess('Python' + str(i))  # 实例化进程对象
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    print('结束测试')
