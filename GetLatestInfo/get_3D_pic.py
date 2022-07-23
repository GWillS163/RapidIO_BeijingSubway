import requests
import os
import re
import bs4


def save_img_by_station_name(station_name, work_dir='./'):
    """
    下载百度百科图片，并保存到本地
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

    for img in imgs:
        img_url = img.find('img').get('data-src').split('?')[0]
        print(img_url)

        # save img by img_url to local file at current path
        img_name = img_url.split('/')[-1][:4]
        img_name = re.sub(r'[\\/:*?"<>|]', '', img_name)
        img_name = station_name + '_' + img_name + ".jpg"
        print(img_name)

        # save to station_name folder if not exist new it
        save_folder = os.path.join(work_dir, station_name)
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        with open(os.path.join(save_folder, img_name), 'wb') as f:
            f.write(requests.get(img_url).content)

if __name__ == '__main__':
    save_img_by_station_name("北京大学东门站")