from pprint import pprint

import requests
import json
from bs4 import BeautifulSoup
# 获取城市id 和 城市名称
"http://webapi.amap.com/subway/data/citylist.json?uid=1658716539543"

# 使用城市id 和 城市拼音获取地铁线路信息
"http://webapi.amap.com/subway/data/{id}_drw_{城市拼音}.json?uid=1658716539821"

# 例如：
"http://webapi.amap.com/subway/data/1100_drw_beijing.json?uid=1658716539821"


def get_City_subway_info(city_id="1100", city_name="beijing"):
    # Method 1. get the latest subway info by API
    # url = f"http://webapi.amap.com/subway/data/{city_id}_drw_{city_name}.json"
    # r = requests.get(url, params={"uid": "1658716539821"},  headers={"User-Agent": "Mozilla/5.0"})
    # r.encoding = "utf-8"
    # json_data = json.loads(r.text)

    # Method2. load local json file
    data = {}
    with open("../data/BJSubway_2022-7-25.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # process json data
    for line in json_data["l"]:
        # print("Line:", line['kn'])
        data.update({line['kn']: []})
        for station in line['st']:
            # print(station['n'])
            station_name = station['n'] + "站" if station['n'].endswith("站") else station['n'] + "站"
            data[line['kn']].append(station_name)
    return data


if __name__ == '__main__':
    pprint(get_City_subway_info())

