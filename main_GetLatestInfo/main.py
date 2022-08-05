import queue
import threading
import time
from functools import partial

from get_subwayInfo_ByAPI import get_City_subway_info
from get_subwayInfo_by_official import *
from get_3D_pic import *

req_baike_tasks = queue.Queue()
req_pic_tasks = queue.Queue()
save_tasks = queue.Queue()
save_info = queue.Queue()


# 2. get the latest stations info
def _get_pic_url():
    """获得站内图片的urls"""
    while req_baike_tasks.qsize() > 0:
        line_name, station_name = req_baike_tasks.get()
        try:
            img_urls = get_img_urls_by_station(station_name)
            staion_folder = os.path.join(save_path, line_name, station_name)
            if not img_urls and not os.path.exists(staion_folder):
                os.mkdir(staion_folder)
            for img_url in img_urls:
                req_pic_tasks.put([img_url, line_name, station_name])
        except Exception as e:
            print(f"Occur {e} during request {line_name} {station_name}\n\n")
            save_info.put(["reqBkError", line_name, station_name, ""])
    print("all of get_pic_url tasks done")


def _request_img():
    while t_req_baike.is_alive():
        img_url, line_name, station_name = req_pic_tasks.get()
        try:
            img_name, img_content = request_img(station_name, img_url)
            save_tasks.put([line_name, station_name, img_name, img_content])
        except Exception as E:
            print(f"Occur {E} during request {line_name} {station_name} {img_url[:-10]}\n\n")
            # save_tasks.put([line_name, station_name, img_name, ""])
            save_info.put(["reqImgError", line_name, station_name, img_url])
    print("all of req_pic_tasks tasks done")


def _save_img(save_path, blocked_list, blocked_folder):
    """还在请求图片时，保持程序不退出"""
    # save to station_name folder if not exist new it
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # while save_tasks.qsize() > 0:
    while t_req_pics.is_alive():
        line_name, station_name, img_name, img_content = save_tasks.get()
        if img_name in blocked_list:
            save_img(blocked_folder, img_name, img_content)
            save_info.put(["BLOCKED", line_name, station_name, img_name])
            continue
        save_img(os.path.join(save_path, line_name), img_name, img_content)
        save_info.put(["OK", line_name, station_name, img_name])

    print("all of save_img tasks done")


def _print_task_queue():
    while t_img_save.is_alive():
        # print with colorful characters
        # print(f"\033[1;31;40m req_baike_tasks:{req_baike_tasks.qsize()} \033[0m")

        [info, line_name, station_name, img_name] = save_info.get()
        if info != "OK":
            print(f"{info} {line_name} {station_name} {img_name}")
        print(f"\r"
              f"reqBkTsk:\033[1;36;40m {req_baike_tasks.qsize():5} \033[0m"
              f"reqPicTsk:\033[4;31;40m {req_pic_tasks.qsize():5} \033[0m"
              f"imgSvTsk:\033[1;32;40m {save_tasks.qsize():5}\033[0m"
              f"savedInf:\033[1;43;40m {info}, {line_name:5} {img_name:<30}\033[0m"
              , end="")

        time.sleep(0.1)
        if save_tasks.qsize() == 0 and req_baike_tasks.qsize() == 0 and req_pic_tasks.qsize() == 0:
            print("all of tasks done")
            break


def get_block_list(blocked_folder):
    # new_blocked_list folder
    if not os.path.exists(blocked_folder):
        os.mkdir(blocked_folder)
        return []

    return os.listdir(blocked_folder)


if __name__ == '__main__':
    # 用户可更改使用路径
    work_path = '../data/'
    block_list = get_block_list("../data/baike_block_img_list")

    # get current date and use it as the folder name
    date = time.strftime("%Y-%m-%d", time.localtime())
    save_path = os.path.join(work_path, date)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_blocked_folder = os.path.join(save_path, "blocked")

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
    t_img_save = threading.Thread(target=partial(_save_img, save_path, block_list, save_blocked_folder))
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


