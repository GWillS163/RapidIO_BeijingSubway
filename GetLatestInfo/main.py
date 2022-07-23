import queue
import threading
import time

from get_latest_stations import *
from get_3D_pic import *
req_baike_tasks = queue.Queue()
req_pic_tasks = queue.Queue()
save_tasks = queue.Queue()


# 2. get the latest stations info
def _get_pic_url():
    while req_baike_tasks.qsize() > 0:
        line_name, station_name = req_baike_tasks.get()
        img_urls = get_img_urls_by_station(station_name)
        for img_url in img_urls:
            req_pic_tasks.put([img_url, line_name, station_name])
    print("all of get_pic_url tasks done")


def _request_img():
    time.sleep(3)
    while True:
        while req_pic_tasks.qsize() > 0:
            img_url, line_name, station_name = req_pic_tasks.get()
            # combine line_name and station_name to get the folder name use os.path.join
            # save_path = os.path.join('./'+line_name, station_name)
            save_path = line_name

            img_name, img_content = request_img(station_name, img_url)
            save_tasks.put([save_path, img_name, img_content])
            # print(f"get_pic_tasks:{line_name} {station_name} {img_name} ")
        if req_pic_tasks.qsize() == 0:
            time.sleep(5)
            if req_pic_tasks.qsize() == 0:
                break
    print("all of req_pic_tasks tasks done")


def _save_img():
    time.sleep(3)
    while True:
        while save_tasks.qsize() > 0:
            save_path, img_name, img_content = save_tasks.get()
            save_img('./'+save_path, img_name, img_content)
            print(f"save_img:{save_path} {img_name}")

        if save_tasks.qsize() == 0:
            time.sleep(5)
            if save_tasks.qsize() == 0:
                break
    print("all of save_img tasks done")


def _print_task_queue():
    while True:
        # print with colorful characters
        # print(f"\033[1;31;40m req_baike_tasks:{req_baike_tasks.qsize()} \033[0m")
        print(f"\r"
              f"\033[1;36;40m req_baike_tasks:{req_baike_tasks.qsize():5} \033[0m"
              f"\033[1;38;40m req_pic_tasks:{req_pic_tasks.qsize():5} \033[0m"
              f"\033[1;32;40m save_tasks:{save_tasks.qsize():5}\033[0m"
              , end="")

        time.sleep(0.1)
        if save_tasks.qsize() == 0 and req_baike_tasks.qsize() == 0 and req_pic_tasks.qsize() == 0:
            print("all of tasks done")
            break


if __name__ == '__main__':
    t_start = time.time()
    # request bjSubway.com
    latest_data = get_latest_stations()
    pprint(latest_data)

    # 1. put all stations into get_pic_tasks
    for line in latest_data.keys():
        # create folder with line name if not exists
        if not os.path.exists(line):
            os.mkdir(line)

        # iterate stations of line. request baidu baike
        for station in latest_data[line]:
            req_baike_tasks.put([line, station])
        print(f"Put stations in {line} done")

    t_get_pic_url = threading.Thread(target=_get_pic_url)
    t_request = threading.Thread(target=_request_img)
    t_save = threading.Thread(target=_save_img)
    t_print = threading.Thread(target=_print_task_queue)
    t_get_pic_url.start()
    t_request.start()
    t_save.start()
    t_print.start()
    t_get_pic_url.join()
    t_request.join()
    t_save.join()
    print("all done, used time:", time.time() - t_start)
