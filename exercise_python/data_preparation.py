import time, json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_token():
    result = requests.post('http://192.168.12.52:9880/security/login',
                           data=json.dumps({"grant_type": "password", "username": "admin",
                                            "password": "Dxnt7dhcz55b/gSWgQWN+Q=="}),
                           headers={"Accept": "application/json, text/plain, */*", "Content-Type": "application/json",
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
                                    "Referer": "http://192.168.12.52:9880/"})
    return result.text


def click_actions(driver):
    start_time=time.time()
    cookie_token = json.loads(get_token())
    userinfo = {"accountId": "admin", "password": "Dxnt7dhcz55b/gSWgQWN+Q==", "security": cookie_token["token"]}
    user = {"user": userinfo}
    js = "window.localStorage.setItem('dct.login.user.token','" + json.dumps(user) + "')"
    driver.execute_script(js)
    time.sleep(5)
    driver.refresh()
    t_xpath = '//ul[@class="header-height ant-menu ant-menu-root ant-menu-dark ant-menu-horizontal ng-star-inserted"]/li'
    click_target = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, t_xpath)))
    # click_target = driver.find_element_by_xpath(t_xpath)
    for t in click_target:
        print(f"click{t.text}")
        t.click()
        time.sleep(500)
        if time.time()-start_time>3000:
            break
    return click_actions(driver)



if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome('./chromedriver')
    driver.get('http://192.168.12.52:9880')
    click_actions(driver)

    driver.quit()
