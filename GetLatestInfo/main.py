import queue
import threading
import time

from GetLatestInfo.get_subwayInfo_ByAPI import get_City_subway_info
from get_subwayInfo_by_official import *
from get_3D_pic import *

req_baike_tasks = queue.Queue()
req_pic_tasks = queue.Queue()
save_tasks = queue.Queue()

save_path = './'


# 2. get the latest stations info
def _get_pic_url():
    """消灭给予的图片任务"""
    while req_baike_tasks.qsize() > 0:
        line_name, station_name = req_baike_tasks.get()
        img_urls = get_img_urls_by_station(station_name)
        # if img_urls is null, make dir with station_name
        if not img_urls and not os.path.exists(station_name):
            os.mkdir(os.path.join(save_path, line_name, station_name))
        for img_url in img_urls:
            req_pic_tasks.put([img_url, line_name, station_name])
    print("all of get_pic_url tasks done")


def _request_img():
    while t_req_baike.is_alive():
        img_url, line_name, station_name = req_pic_tasks.get()

        img_name, img_content = request_img(station_name, img_url)
        save_tasks.put([line_name, station_name, img_name, img_content])
        # print(f"get_pic_tasks:{line_name} {station_name} {img_name} ")
    # if req_pic_tasks.qsize() == 0:
    #     time.sleep(5)
    #     if req_pic_tasks.qsize() == 0:
    #         break
    print("all of req_pic_tasks tasks done")


def _save_img():
    """还在请求图片时，保持程序不退出"""
    # while save_tasks.qsize() > 0:
    while t_req_pics.is_alive():
        line_name, station_name, img_name, img_content = save_tasks.get()
        save_img(os.path.join(save_path, line_name), img_name, img_content)
        # print(f"save_img:{save_path} {img_name}")

    # if save_tasks.qsize() == 0:
    #     time.sleep(10)
    #     if save_tasks.qsize() == 0:
    #         break
    print("all of save_img tasks done")


def _print_task_queue():
    while t_img_save.is_alive():
        # print with colorful characters
        # print(f"\033[1;31;40m req_baike_tasks:{req_baike_tasks.qsize()} \033[0m")
        print(f"\r"
              f"req_baike_tasks:\033[1;36;40m {req_baike_tasks.qsize():5} \033[0m"
              f"req_pics_tasks:\033[4;31;40m {req_pic_tasks.qsize():5} \033[0m"
              f"img_save_tasks:\033[1;32;40m {save_tasks.qsize():5}\033[0m"
              , end="")

        time.sleep(0.1)
        if save_tasks.qsize() == 0 and req_baike_tasks.qsize() == 0 and req_pic_tasks.qsize() == 0:
            print("all of tasks done")
            break


if __name__ == '__main__':
    # 用户可更改使用路径
    save_path = '../'

    # get current date and use it as the folder name
    date = time.strftime("%Y-%m-%d", time.localtime())
    save_path = os.path.join(save_path, date)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    t_start = time.time()
    # request bjSubway.com
    # latest_data = get_latest_BjSubway_Line()
    latest_data = get_City_subway_info()
    pprint(latest_data)

    # 1. put all stations into get_pic_tasks
    for line in latest_data.keys():
        # create folder with line name if not exists
        line_save_path = os.path.join(save_path, line)
        if not os.path.exists(line_save_path):
            os.mkdir(line_save_path)

        # iterate stations of line. request baidu baike
        for station in latest_data[line]:
            req_baike_tasks.put([line, station])
        print(f"Put stations in {line:10}\t({len(latest_data[line]):4}) done")

    t_req_baike = threading.Thread(target=_get_pic_url)
    t_req_pics = threading.Thread(target=_request_img)
    t_img_save = threading.Thread(target=_save_img)
    t_print = threading.Thread(target=_print_task_queue)
    t_req_baike.start()
    t_req_pics.start()
    t_img_save.start()
    t_print.start()
    # t_req_baike.join()
    # t_req_pics.join()
    # t_img_save.join()
    t_print.join()
    print("all done, used time:", time.time() - t_start)
