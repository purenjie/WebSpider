import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool

def get_page(offset):
    headers = {
        'cookie': 'tt_webid=6846644934884197895; s_v_web_id=verify_kcbn7age_jHFkXSQn_FycR_4FTe_BuOp_ujyfeh4mD1eS; SLARDAR_WEB_ID=9a424e05-bcd1-45f8-b8c8-b2e98f5b02dc; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=31ts0cvd91594108771233; tt_webid=6846644934884197895; csrftoken=eb64bbc46c2365a17135b707161b241b; __ac_nonce=05f042ce300b84d7cfe66; __ac_signature=_02B4Z6wo00f01FuaHkwAAIBDcgo4wAw-H4hbnhrAAEnnk04LCQy7sXZn8I0gowYBdAnc0NbH87vvu.6sOMRmu9nAOVLEng6BK0ovLcI6Ozj2ToJVL7CJSOrc5dn9Ui6jFGdj-6CYVgL8JVcm64; tt_scid=Q5QUIb-pj0UCXquuvRiP4k7yHs0idHEpNgi6Af0VR75hsDA42LYbifnh-7wUZmn2c716',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D'
    }
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(params)
    # print(url)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            if item.get('image_list'):
                for image in item['image_list']:
                    yield {
                        'image': image.get('url'),
                        'title': title
                    }


def save_image(item):
    path = os.path.join('jiepai', item.get('title')) 
    if not os.path.exists(path):
        # os.mkdir(item.get('title'))
        os.makedirs(path) # 创建多层目录

    response = requests.get(item.get('image'))
    if response.status_code == 200:
        file_path = '{0}/{1}.{2}'.format(path, md5(response.content).hexdigest(), 'jpg')
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(response.content)
        else:
            print('Already Downladed', file_path)




def main(offset):
    json = get_page(offset)
    for image in get_images(json):
        print(image)
        save_image(image)

GROUP_START = 1
GROUP_END = 20

if __name__=='__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END+1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
