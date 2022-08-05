import os
import queue
import time
from multiprocessing import Process


from get_3D_pic import get_img_urls_by_station


class ReqUrlsProcess(Process):  # 继承Process类
    def __init__(self, name, station_name, save_path, line_name):
        super(ReqUrlsProcess, self).__init__()
        self.name = name
        self.station_name = station_name
        self.save_path = save_path
        self.line_name = line_name
        self.img_urls = []

    def run(self):
        global req_baike_tasks
        img_urls = get_img_urls_by_station(self.station_name)
        station_folder = os.path.join(self.save_path, self.line_name, self.station_name)
        if not img_urls and not os.path.exists(station_folder):
            os.mkdir(station_folder)
        self.img_urls = img_urls
        # for img_url in img_urls:
        #     req_baike_tasks.put([img_url, self.line_name, self.station_name])

    def get_img_urls(self):
        return self.img_urls

    def __del__(self):
        pass


if __name__ == '__main__':
    req_pic_tasks = queue.Queue()
    urlsP = ReqUrlsProcess("reqBK", "马各庄站", ".", "地铁燕房线")
    urlsP.start()
    urlsP.join()
    print('结束测试')




