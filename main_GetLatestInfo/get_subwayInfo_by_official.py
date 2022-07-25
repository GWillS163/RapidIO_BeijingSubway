from pprint import pprint

import requests
from bs4 import BeautifulSoup


def get_latest_BjSubway_Line():
    """
    get the latest station infos from https://www.bjsubway.com/
    :return:
    """
    data = {}
    # TODO: 缺少四号线线路
    url = "https://www.bjsubway.com/station/xltcx/"
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})
    html = res.text.encode('iso-8859-1').decode('gbk')
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    line_name = ""
    all_elem = soup.find('div', class_='line_content')
    for elem in all_elem.find_all('div'):
        attribute = elem.__getattribute__('attrs')['class'][0]
        value = elem.text.strip().replace('/', '_')
        if attribute == "line_name":
            print("line_name:", value)
            line_name = value
            data[line_name] = []
        elif attribute == "station":
            print("station:", value)
            data[line_name].append(value+"站")
        else:
            print("other:", value)

    return data


def get_latest_mtrBJ_Line():
    """
    403 Forbidden
    get the latest station infos from http://www.mtr.bj.cn/service
    :return:
    """
    data = {}
    site = "http://www.mtr.bj.cn"
    catalog = "/service"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    res = requests.get(site + catalog, headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')

    lines = soup.find_all("div", class_="line-header")
    for line in lines:
        line_name = line.find("div", class_="line-name").text.split(" ")[0]
        line_link = line.find("a").get("href")
        data.update({line_name: []})
        print("line_name:", line_name)

        # get the station info of the line
        # TODO: 403 Forbidden:
        line_res = requests.get(site + line_link, headers=header)
        line_soup = BeautifulSoup(line_res.text, 'html.parser')
        stations_div = line_soup.find("div", class_="stations")
        stations = stations_div.find_all("a")
        for station in stations:
            station_name = station.text.strip()
            data[line_name].append(station_name)
    return data


if __name__ == '__main__':

    # run function above
    # latest_data = get_latest_BjSubway_Line()
    latest_data = get_latest_mtrBJ_Line()
    pprint(latest_data)
