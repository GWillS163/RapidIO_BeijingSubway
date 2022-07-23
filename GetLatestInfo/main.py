from get_latest_stations import *
from get_3D_pic import *

if __name__ == '__main__':
    # request bjSubway.com
    latest_data = get_latest_stations()
    pprint(latest_data)
    for line in latest_data.keys():
        # create folder with line name if not exists
        if not os.path.exists(line):
            os.mkdir(line)
        # iterate stations of line. request baidu baike
        for station in latest_data[line]:
            save_img_by_station_name(station, line)
        print(f"{line} done")
    print("all done")
    