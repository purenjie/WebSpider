import json
import requests
from requests.exceptions import RequestException
import re
import time
from lxml import etree
import csv


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }

def xpath_parse(html):
    html = etree.HTML(html)
    index = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/i//text()')
    image = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/a/img[2]/@data-src')
    title = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[1]/p[1]/a/text()')
    actor = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[1]/p[2]/text()')
    actor = list(map(lambda x: x.replace('/n', '').strip(), actor))
    time = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[1]/p[3]/text()')
    score_1 = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[2]/p/i[1]/text()')
    score_2 = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[2]/p/i[2]/text()')
    score = list(map(lambda x: x[0]+x[1], zip(score_1, score_2)))
    
    json_dict = {}
    for i in range(10):
        json_dict["index"] = index[i]
        json_dict["image"] = image[i]
        json_dict["title"] = title[i]
        json_dict["actor"] = actor[i]
        json_dict["time"] = time[i]
        json_dict["score"] = score[i]
        yield json_dict
        



def write_to_json(json_dict):
    with open('maoyan_100_movies.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, indent=4, ensure_ascii=False) + '\n')

def write_to_csv(json_dict):
    with open('maoyan_100_movies.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 第一次添加列名
        global flag
        if flag:
            writer.writerow(['index', 'image_url', 'title', 'actor', 'time', 'score'])
            flag = False
        
        item = []
        for key in json_dict:
            item.append(json_dict[key])
        writer.writerow(item)



def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    
    # for item in parse_one_page(html):
    for item in xpath_parse(html):
        print(item)
        # write_to_json(item)
        write_to_csv(item)


if __name__ == '__main__':
    flag = True
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)