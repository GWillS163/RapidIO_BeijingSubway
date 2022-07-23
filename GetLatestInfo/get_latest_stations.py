from pprint import pprint

import requests
from bs4 import BeautifulSoup


def get_latest_stations():
    """
    get the latest station infos from https://www.bjsubway.com/
    :return:
    """
    data = {}

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


if __name__ == '__main__':

    # run function above
    latest_data = get_latest_stations()
    pprint(latest_data)
