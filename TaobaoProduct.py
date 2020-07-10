#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   TaobaoProduct.py
@Time    :   2020/07/08 16:24:42
@Author  :   Solejay 
@Version :   1.0
@Contact :   prj960827@gmail.com
@Desc    :   64 行手动 debug 输入验证码，生成 dict 没有存储到数据库或者 json 文件
'''

# here put the import lib


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
# from config import *
from urllib.parse import quote
import time
from selenium.webdriver.support import expected_conditions as EC
import requests
import json


def get_products(browser):
    """
    提取商品数据
    """
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_json(product)


def index_page(page):
    print('正在爬取第', page, '页')
    browser.get("https://s.taobao.com/search?q=iPad")
    if page == 1:
        #chrome_options.add_argument('--headless')
        # 下一行代码是为了以开发者模式打开chrome
        # 通过微博方式登录账号
        button = browser.find_element_by_xpath('//*[@id="login-form"]/div[5]/a[1]')
        button.click()
        user_name = browser.find_element_by_name('username')
        user_name.clear()
        user_name.send_keys('xxxxxx') #输入微博名 需要事先绑定淘宝
        time.sleep(1)
        user_keys = browser.find_element_by_name('password')
        user_keys.clear()
        user_keys.send_keys('xxxxxx') #输入微博密码
        time.sleep(1)
        verifycode = browser.find_element_by_name('verifycode')
        verifycode.clear()
        verifycode.send_keys('abcd')
        button = browser.find_element_by_class_name('W_btn_g')
        button.click()
        time.sleep(1)
        cookies = browser.get_cookies()
        ses=requests.Session() # 维持登录状态
        c = requests.cookies.RequestsCookieJar()
        for item in cookies:
            c.set(item["name"],item["value"])
            ses.cookies.update(c)
            ses=requests.Session()
            time.sleep(1)
        print('登录成功')

    if page > 1:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        
    return(get_products(browser))

def save_to_json(result):
    with open('TaobaoProduct.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(result, indent=4, ensure_ascii=False) + '\n')


def main():
    """
    遍历每一页
    """
    for i in range(1, 10 + 1):
        index_page(i)
    browser.close()




chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
browser = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(browser, 30)
# main()
index_page(1)
