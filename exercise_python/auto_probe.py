#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time,traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
try:
    browser=webdriver.Chrome(executable_path='chromedriver_win32_90/chromedriver.exe',chrome_options=chrome_options)
    browser.implicitly_wait(5)
    browser.get('http://192.168.12.9:8082/job/cloudops-aio-new')
    # html=browser.page_source
    # print(html)
    element=browser.find_element_by_xpath('//a[@href="/job/cloudops-aio-new/build?delay=0sec" and @class="task-link "]')
    # element.click()
    print(element.get_attribute('title'))
    time.sleep(2)
except:
    traceback.print_exc()
finally:
    browser.quit()
