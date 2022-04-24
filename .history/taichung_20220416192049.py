from audioop import add
from email.policy import strict
from selenium import webdriver
from time import sleep
import pandas as pd
import numpy as np
from selenium.webdriver import ActionChains

options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
driver = webdriver.Chrome('/Users/wangyoujun/Desktop/assignment3/chromedriver')
driver.maximize_window()
url = "https://www.agoda.com/zh-tw/"
driver.get(url)
driver.implicitly_wait(20)
driver.find_element_by_xpath(
    "//*[text()='等下再說']").click()
driver.implicitly_wait(20)
driver.find_element_by_css_selector(
    "[class='SearchBoxTextEditor SearchBoxTextEditor--autocomplete']").send_keys('台中市')
taipei = driver.find_element_by_xpath("//*[@data-text='台中市']")
taipei.click()
chains = ActionChains(driver)
chains.move_by_offset(1, 1).perform()
chains.double_click().perform()
driver.find_element_by_xpath("//*[@data-element-name='search-button']").click()
driver.implicitly_wait(20)
driver.find_element_by_xpath(
    "//*[@class='Buttonstyled__ButtonStyled-sc-5gjk6l-0 kYHirW Box-sc-kv6pi1-0 hVPGaU']").click()
id = []
address = []
temp_height = 0
count = 0
while True:
    sleep(5)
    while True:
        driver.execute_script("window.scrollBy(0,1000)")
        sleep(2)
        y = driver.find_element_by_class_name('Address__Text')
        for i in range(len(y)):
            if y[i] not in address:
                address.append(y[i])
            
        check_height = driver.execute_script(
            "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        if check_height == temp_height:
            break

        temp_height = check_height
        print(check_height)
    # 滾到底了
    x = driver.find_elements_by_css_selector(
        "[class='PropertyCard PropertyCardItem']")

    for i in range(len(x)):
        if x[i].get_attribute("data-hotelid") not in id:
            id.append(x[i].get_attribute("data-hotelid"))
    count = count + 1
    print("-------------------page"+" "+str(count) +
          "-------------------累積資料數"+" "+str(len(id)))
    for i in range(len(id)):
        print(str(id[i])+str(address[i]))
    # 跳頁
    try:
        next = driver.find_element_by_id("paginationNext")
        next.click()
    except Exception:
        print("maybe something wrong")
        break
# # 最後資訊
# print("-------------------fianl-------------------共"+str(len(id))+"筆資料")
# for i in range(len(id)):
#     print(id[i])
# hotelnumpy = np.array(id)
# allhotel = pd.DataFrame(hotelnumpy, columns=['hotelid'])
# allhotel.to_csv("taichung.csv", encoding='utf_8_sig')
