'''
图像验证码识别
'''
# import tesserocr
# from PIL import Image
# # 图形验证码 tesserocr 效果一般
# image = Image.open('code2.jpg')
# image = image.convert('L')
# threshold = 127
# table = []
# for i in range(256):
#     if i < threshold:
#         table.append(0)
#     else:
#         table.append(1)
# image = image.point(table, '1')
# image.show()
# result = tesserocr.image_to_text(image)
# print(result)

'''
极验滑动验证码识别
'''
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

email = 'test@test.com'
password = '123456'

class CrackGeetest():
    def __init__(self):
        self.url = 'https://auth.geetest.com/login/'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = email
        self.password = password

    def get_geetest_button(self):
        '''
        获取初始验证按钮
        返回按钮对象
        '''
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 20)
browser.get('https://auth.geetest.com/login/')

email = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[3]/div/form/div[1]/div/div[1]/input')))
email.clear()
email.send_keys('747688845@qq.com')
password = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[3]/div/form/div[2]/div/div[1]/input')))
password.clear()
password.send_keys('123456')
button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
button.click()



