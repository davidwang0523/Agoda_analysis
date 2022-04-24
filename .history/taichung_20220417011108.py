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
taichung = driver.find_element_by_xpath("//*[@data-text='台中市']")
taichung.click()
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
check = 0
taichungframe = pd.DataFrame(columns=['飯店編號', '距離市中心'])
while True:
    sleep(5)
    scrollcount = 0
    temp_scroll = []
    temp = []
    # 滾動視窗
    while True:
        driver.execute_script("window.scrollBy(0,1000)")
        check_height = driver.execute_script(
            "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        sleep(2)
        y = driver.find_elements_by_class_name('Address__Text')  # 此次scroll的結果
        f = []
        for i in range(len(y)):
            f.append(y[i].text)  # 建立一列
            if i == len(y)-1:
                if scrollcount == 0:
                    temp_scroll.append(f)
                    print(temp_scroll)
                    print("---------------------")
                    # 第一次的滾動結果加入暫存
                else:  # 若不是第一次 則加上 上次滾動的結果到下一列
                    temp_scroll.append(temp_scroll[scrollcount-1]+f)
                    print(temp_scroll)
                    print("---------------------")
        scrollcount += 1
        if check_height == temp_height:
            break

        temp_height = check_height
        print(check_height)

    for i in range(scrollcount):
        print(temp_scroll[i])
        if i == 0:  # 第一次的滾動結果加入temp
            for j in range(len(temp_scroll[i])):
                temp.append(temp_scroll[i][j])

        else:  # 不是第一次
            for j in range(len(temp_scroll[i])):  # 跑至下一次的列長度
                if j <= len(temp_scroll[i-1]):  # 尚未跑到本身的列長度 跳過
                    continue
                else:  # 已經跑到了
                    temp.append(temp_scroll[i][j])  # 加入temp

    #滾到底了
    x = driver.find_elements_by_css_selector(
        "[class='PropertyCard PropertyCardItem']")

    print(len(x))
    print(len(temp))
    for i in range(len(x)):
        if x[i].get_attribute("data-hotelid") not in id:
            id.append(x[i].get_attribute("data-hotelid"))
            address.append(temp[i])

    count = count + 1
    check += 1
    print("-------------------page"+" "+str(count) +
          "-------------------累積資料數"+" "+str(len(id)))

    for i in range(len(id)):
        print(str(id[i])+str(address[i]))
        taichungframe = taichungframe.append(
            {'飯店編號': str(id[i]), '距離市中心': str(address[i])}, ignore_index=True)
    # 跳頁
    try:
        next = driver.find_element_by_id("paginationNext")
        next.click()
    except Exception:
        print("maybe something wrong")
        break
    if check == 1:
        break

# 最後資訊
print("-------------------fianl-------------------共"+str(len(id))+"筆資料")
for i in range(len(id)):
    print(str(id[i])+str(address[i]))
taichungframe.to_csv("taichungframe.csv", encoding='utf_8_sig')
