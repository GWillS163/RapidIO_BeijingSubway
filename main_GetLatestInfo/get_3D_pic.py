import requests
import os
import re
import bs4
from request_multiProcessing import MyProcess


def get_img_urls_by_station(station_name):
    """
    获得百度百科图片urls
    例: https://baike.baidu.com/item/人民大学站
    :param station_name:
    :return:
    """

    # Baidu Baike
    url = 'https://baike.baidu.com/item/' + station_name
    res = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    imgs = soup.findAll('a', class_='image-link')

    img_urls = []
    for img in imgs:
        img_url = img.find('img').get('data-src').split('?')[0]
        img_urls.append(img_url)
    return img_urls


def request_img(station_name, img_url):
    # save img by img_url to local file at current path
    img_name = img_url.split('/')[-1][:4]
    img_name = re.sub(r'[\\/:*?"<>|]', '', img_name)
    img_name = station_name + '_' + img_name + ".jpg"
    return img_name, requests.get(img_url).content


def save_img(path, img_name, img_content):
    # # if img_content's size is too small, pass it
    # if len(img_content) < 1024:
    #     return

    if not os.path.exists(path):
        os.mkdir(path)
    # save img to local file if not exist
    if not os.path.exists(path + img_name):
        with open(os.path.join(path, img_name), 'wb') as f:
            f.write(img_content)

if __name__ == '__main__':
    get_img_urls_by_station("北京大学东门站")
