import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq


base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
# client = MongoClient()
# db = client['weibo']
# collection = db['weibo']
MAX_PAGE = 10


def get_page(since_id):
    params = {
        # 'type': 'uid',
        # 'value': '2830678474',
        'containerid': '1076032830678474',
    }

    if since_id!=0:
        params['since_id'] = since_id

    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json(), page
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json, page: int):
    if json:
        items = json.get('data').get('cards')
        for index, item in enumerate(items):
            if page == 1 and index == 1:
                continue
            else:
                item = item.get('mblog', {})
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_count')
                yield weibo


# def save_to_mongo(result):
#     if collection.insert(result):
#         print('Saved to Mongo')

def save_to_json(result):
    with open('weibo.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(result, indent=4, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    since_id = 0
    for page in range(1, MAX_PAGE + 1):
        json = get_page(since_id)
        since_id = json[0].get('data').get('cardlistInfo').get('since_id')
        results = parse_page(*json)
        for result in results:
            print(result)
            # save_to_json(result)



