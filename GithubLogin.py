#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   GithubLogin.py
@Time    :   2020/07/09 14:45:58
@Author  :   Solejay 
@Version :   1.0
@Contact :   prj960827@gmail.com
@Desc    :   实现 github 模拟登陆并查看主页动态
'''

# here put the import lib

import requests
from lxml import etree
import re

from requests.api import head

def login(email, password):
    post_data = {
        'commit': 'Sign in',
        'authenticity_token': token,
        'ga_id': '786651390.1594257181',
        'login': email,
        'password': password,
        "webauthn-support": "supported",
        'webauthn-iuvpaa-support': 'unsupported',
        'return_to': '',
        'required_field_6796': ''
    }
    response = session.post(post_url, data=post_data, headers=headers)
    response = session.get(feed_url, headers=headers)
    if response.status_code == 200:
        dynamics(response.text)
    response = session.get(logined_url, headers=headers)
    if response.status_code == 200:
        profile(response.text)

def dynamics(html):
    print('*'*10+'dynamicing'+'*'*10)
    selector = etree.HTML(html)
    # print("*"*20, etree.tostring(selector).decode('utf-8'))
    # print(selector.xpath('//div[@class="d-flex flex-items-baseline"]'))
    dynamics = selector.xpath('//div[@class="d-flex flex-items-baseline"]//div')
    # print(dynamics)
    for item in dynamics:
        etree.strip_elements(item, 'span')
        dynamic = ' '.join(item.xpath('.//text()')).replace('\n', ' ').strip()
        dynamic = re.sub(' +', ' ', dynamic)
        print(dynamic)
        write_to_txt(dynamic)
    print('*' * 10 + 'dynamic end' + '*' * 10)

def profile(html):
    print('*'*10+'profileing'+'*'*10)
    selector = etree.HTML(html)
    name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
    email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')[0]
    print(name, email)
    write_to_txt(name + ' ' + email)

login_url = 'https://github.com/login'
post_url = 'https://github.com/session'
feed_url = 'https://github.com/dashboard-feed'
logined_url = 'https://github.com/settings/profile'


headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 OPR/62.0.3331.43',
            'Host': 'github.com'
        }

def write_to_txt(content):
    with open('GithubLogin.txt', 'a', encoding='utf-8') as f:
        f.write(content + '\n')

# 获取 authenticity_token
session = requests.Session()
response = session.get(login_url, headers=headers)
selector = etree.HTML(response.text)
token = selector.xpath('//*[@id="login"]/form/input[1]/@value')[0]
print(token)
write_to_txt(token)


email = 'prj960827@gmail.com'
password = '123456'
login(email, password)






