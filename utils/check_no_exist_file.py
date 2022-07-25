
# get file list of dir
import json
import os
from data.uncomplete_map import map

def check_no_exist_file(dir, map):

    line_list = os.listdir(dir)
    for line in line_list:
        file_list = os.listdir(os.path.join(dir, line))

        # check file exist
        new_file_lst = [file.split('_')[0] for file in file_list]
        for station in map[line]:
            if station in new_file_lst:
                continue
            new_folder = os.path.join(dir, line, station)
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
                print("new_folder:", new_folder)


if __name__ == '__main__':
    dir = '../2022-07-25/'
    # map
    from data.completed_map import map
    check_no_exist_file(dir, map)
