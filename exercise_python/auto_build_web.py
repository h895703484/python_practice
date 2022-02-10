import time,traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
try:
    browser=webdriver.Chrome(executable_path='chromedriver_win32_92/chromedriver.exe',chrome_options=chrome_options)
    browser.implicitly_wait(5)
    browser.get('http://192.168.12.9:8082/job/cloudops_platform_build_branch')
    # html=browser.page_source
    # print(html)
    element=browser.find_element_by_xpath('//a[@href="/job/cloudops_platform_build_branch/build?delay=0sec" and @class="task-link "]')
    element.click()
    s_element=WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//select[@id="gitParameterSelect"]')))
    # s_element=browser.find_element_by_xpath('//select[@id="gitParameterSelect"]')
    print(s_element.get_attribute('name'))
    s=Select(s_element)
    s.select_by_visible_text('origin/master')
    build_start=browser.find_element_by_xpath('//button[@id="yui-gen1-button"]')
    print(build_start.get_attribute('id'))
    # build_start.click()
    # time.sleep(2)
except:
    traceback.print_exc()
finally:
    browser.quit()