from tkinter.ttk import Style
import requests
from audioop import add
from email.policy import strict
from selenium import webdriver
from time import sleep
import pandas as pd
import numpy as np
from selenium.webdriver import ActionChains
import matplotlib.pyplot as plt
import warnings
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing, Holt
warnings.filterwarnings('ignore')
# options = webdriver.ChromeOptions()
# options.add_argument(
#     'user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
# driver = webdriver.Chrome('/Users/wangyoujun/Desktop/assignment3/chromedriver')
# driver.maximize_window()
# url = "https://www.agoda.com/zh-tw/"
# driver.get(url)
# driver.implicitly_wait(20)
# driver.find_element_by_xpath(
#     "//*[text()='等下再說']").click()
# driver.implicitly_wait(20)
# driver.find_element_by_css_selector(
#     "[class='SearchBoxTextEditor SearchBoxTextEditor--autocomplete']").send_keys('台中市')
# taichung = driver.find_element_by_xpath("//*[@data-text='台中市']")
# taichung.click()
# chains = ActionChains(driver)
# chains.move_by_offset(1, 1).perform()
# chains.double_click().perform()
# driver.find_element_by_xpath("//*[@data-element-name='search-button']").click()
# driver.implicitly_wait(20)
# driver.find_element_by_xpath(
#     "//*[@class='Buttonstyled__ButtonStyled-sc-5gjk6l-0 kYHirW Box-sc-kv6pi1-0 hVPGaU']").click()
# id = []
# address = []
# temp_height = 0
# count = 0
# taichungframe = pd.DataFrame(columns=['飯店編號', '距離市中心'])
# while True:
#     sleep(5)
#     # 滾動視窗
#     while True:
#         driver.execute_script("window.scrollBy(0,1000)")
#         check_height = driver.execute_script(
#             "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
#         sleep(2)

#         if check_height == temp_height:
#             break

#         temp_height = check_height
#         print(check_height)


#     #滾到底了
#     sleep(5)
#     x = driver.find_elements_by_css_selector(
#         "[class='PropertyCard PropertyCardItem']")
#     y = driver.find_elements_by_class_name('Address__Text')  # 此次scroll的結果
#     print(len(x))
#     print(len(y))
#     for i in range(len(x)):
#         if x[i].get_attribute("data-hotelid") not in id:
#             id.append(x[i].get_attribute("data-hotelid"))
#             address.append(y[i].text)

#     count = count + 1
#     print("-------------------page"+" "+str(count) +
#           "-------------------累積資料數"+" "+str(len(id)))

#     for i in range(len(id)):
#         print(str(id[i])+str(address[i]))
#     # 跳頁
#     try:
#         next = driver.find_element_by_id("paginationNext")
#         next.click()
#     except Exception:
#         print("maybe something wrong")
#         break

# # 最後資訊
# print("-------------------fianl-------------------共"+str(len(id))+"筆資料")
# for i in range(len(id)):
#     print(str(id[i])+str(address[i]))
#     taichungframe = taichungframe.append(
#             {'飯店編號': str(id[i]), '距離市中心': str(address[i])}, ignore_index=True)
# taichungframe.to_csv("taichungframe.csv", encoding='utf_8_sig')

x = pd.read_csv('taichungframe.csv')

# 個別抓取hotelreview
urlhotelreview = 'https://www.agoda.com/api/cronos/property/review/HotelReviews'
cookies = 'agoda.user.03=UserId=19c0f0da-ec11-4105-b2ef-e45a59a5333b; agoda.prius=PriusID=0&PointsMaxTraffic=Agoda; agoda.vuser=UserId=ac74e42f-394b-4e73-a9c3-257399b0a755; agoda.price.01=PriceView=1; _ab50group=GroupA; _40-40-20Split=Group40A; deviceId=8fe74881-b446-4c85-b764-06cb1f6fbdf6; FPID=FPID2.2.beyCORSRdx7deaNHdIcVRHZfLRUs7d8qaFgCn5NvkUA%3D.1649368247; ab.storage.userId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%2219c0f0da-ec11-4105-b2ef-e45a59a5333b%22%2C%22c%22%3A1649368249731%2C%22l%22%3A1649368249731%7D; ab.storage.deviceId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%2238aae9b2-d64a-29b3-0f56-7bc3c654483e%22%2C%22c%22%3A1649368249733%2C%22l%22%3A1649368249733%7D; _gcl_aw=GCL.1649368250.Cj0KCQjwl7qSBhD-ARIsACvV1X2rG42go0pjnByn50yuxtdX2sLvJQxvHOxk5vxU0FLZVKvABXNgkKwaAsxQEALw_wcB; _fbp=fb.1.1649368249919.1064921551; agoda.familyMode=Mode=0; _cc_id=84017fc8b983ce28562b5dcc46a4ba56; __gads=ID=8b46d7cb43d44b71:T=1649681029:S=ALNI_MarLpuNwWTwCTWSe6SP0KSjQTi6Jg; agoda.lastclicks=1891473||c6cac438-31ac-9b9f-bc08-0b36bc6fdc3f||2022-04-12T13:54:59||0vxn5khcnlgnh2rc2p44hbow||{"IsPaid":true,"gclid":"CjwKCAjwo8-SBhAlEiwAopc9W6-L_TX-afku7hHGwcYf1KGDZLHwR87KbBWYsCtO3yg-dJfRMahPGxoC24YQAvD_BwE","Type":""}; _gac_UA-6446424-30=1.1649767798.CjwKCAjwo8-SBhAlEiwAopc9W6-L_TX-afku7hHGwcYf1KGDZLHwR87KbBWYsCtO3yg-dJfRMahPGxoC24YQAvD_BwE; _ha_aw=GCL.1649767798.CjwKCAjwo8-SBhAlEiwAopc9W6-L_TX-afku7hHGwcYf1KGDZLHwR87KbBWYsCtO3yg-dJfRMahPGxoC24YQAvD_BwE; _hab_aw=GCL.1649767798.CjwKCAjwo8-SBhAlEiwAopc9W6-L_TX-afku7hHGwcYf1KGDZLHwR87KbBWYsCtO3yg-dJfRMahPGxoC24YQAvD_BwE; agoda.firstclicks=-1||||2022-04-15T19:37:50||m5wzerhue0xfigjiiu5bhr4e||{"IsPaid":false,"gclid":"","Type":""}; agoda.version.03=CookieId=2d778f84-a972-43b3-9eac-4e707a7b65ef&AllocId=616c671cb15bc9323f6324238fdc7b1a0ade648209ebfe5e0b0b56e327675d0babb84cc7086fd074548c81a16e9191c82a8c7c44d37d5681cf18bcd7f57da09542da5924289895c93c168bf1a3d69e8d51a7e7f76a2d778f84a9723b3eac4e707a7b65ef&DLang=zh-tw&CurLabel=TWD&DPN=1&Alloc=&FEBuildVersion=&TItems=2$-1$04-15-2022 19:37$05-15-2022 19:37$&CuLang=20; agoda.attr.03=ATItems=1891473$04-12-2022 13:54$c6cac438-31ac-9b9f-bc08-0b36bc6fdc3f|-1$04-15-2022 19:37$; agoda.landings=-1|||m5wzerhue0xfigjiiu5bhr4e|2022-04-15T19:37:50|False|19----1891473|c6cac438-31ac-9b9f-bc08-0b36bc6fdc3f|CjwKCAjwo8-SBhAlEiwAopc9W6-L_TX-afku7hHGwcYf1KGDZLHwR87KbBWYsCtO3yg-dJfRMahPGxoC24YQAvD_BwE|0vxn5khcnlgnh2rc2p44hbow|2022-04-12T13:54:59|True|20-----1|||m5wzerhue0xfigjiiu5bhr4e|2022-04-15T19:37:50|False|99; ASP.NET_SessionId=m5wzerhue0xfigjiiu5bhr4e; xsrf_token=CfDJ8Dkuqwv-0VhLoFfD8dw7lYzJxRaLYvQMGQSztzmBREC3sYYq9VpjrVjFZfwZr3jaESeAiBucrWpvUBeKI8vw5RB-VpW2yec-4hc9XNlfc09Ph5x6SuSJbAYEZ98m-9BgiRvqwlm0zzy4z5aagS1nIpg; tealiumEnable=true; _gid=GA1.2.1913436381.1650026269; _gat_UA-6446424-30=1; _gat_t3=1; panoramaId_expiry=1650631074741; panoramaId=8bd48870f795076cdccb27d885db16d53938724ce71956636538fee52d6f20df; _gali=SearchBoxContainer; _ga_T408Z268D2=GS1.1.1650026268.19.1.1650026276.52; _ga=GA1.2.2092144022.1649368247; agoda.search.01=SHist=4$908412$7776$1$1$2$0$0$$|4$4846518$7776$1$1$2$0$0$$|1$4951$7776$1$1$2$0$0$$|4$9786373$7779$1$1$2$0$0$$|4$908412$7779$1$1$2$0$0$$|1$4951$7779$1$1$2$0$0$$|4$4846518$7779$1$1$2$0$0$$&H=7774|7$908412$4846518|4$9786373$908412|0$4846518; ab.storage.sessionId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%22efdb0898-62b6-1b85-f763-14f4740ed1c3%22%2C%22e%22%3A1650028077838%2C%22c%22%3A1650026271481%2C%22l%22%3A1650026277838%7D; _clck=1aofcyd|1|f0n|0; _uetsid=dd8c9930bcb811ec88b13363c109d75a; _uetvid=c9e5ac00b6bc11ecb5808de12fb19cb0; cto_bundle=q3z4019yZiUyRkVmS3JFcmJTRlFMeE1Wa0E1JTJCS05rejBPJTJGbWNqMXJTZUF1JTJCaE4yNmhTQmI2ckl1SWFmalM2NmNadmJZb21lbDhUa0NCWmc1TWdtMFBjYTRWMmFSdFVDSXRSVnk2ZTBpODAzTk5MQ3VkTG1xbjNUV21wdHprcXMyendMUjl5bGdUcDFGd3pQVCUyQnl5cnZlaXNreldHZnhKWkFOREZOQm14alg0eW5hS2Y0VGlEeHpiZ09tUyUyRmFoMlZCTXZHd0Q; _clsk=15h16m6|1650026282072|1|0|h.clarity.ms/collect; agoda.analytics=Id=2067492539735259276&Signature=578659147167551467&Expiry=1650029897034; utag_main=v_id:018006022904001a444f03523300050790118071009dc$_sn:16$_se:7$_ss:0$_st:1650028095096$ses_id:1650026268484%3Bexp-session$_pn:4%3Bexp-session'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
    'ag-language-locale': 'zh-tw',
    'accept-language-id': '20',
    'accept-language': 'zh-tw',
    'content-type': 'application/json; charset=UTF-8',
    'Cookie': cookies
}


def set_page(hotelId, page_number):
    r = requests.post(urlhotelreview,
                      json={"hotelId": hotelId, "providerId": 332, "demographicId": 0, "page": page_number,
                            "pageSize": 20,
                            "sorting": 5}, headers=headers)
    temp = r.json()
    return temp

# 設定爬40頁,將每頁的繁體中文資料(台灣)爬完


def hotelinfocrawler(hotelid, distance):
    hotelnodatacount = pd.DataFrame(columns=['飯店名稱', '共幾筆評論'])
    frame = pd.DataFrame(
        columns=['飯店名稱', '距離市中心', '房客名稱', '房客評論', '評分', '停留時間', 'checkin'])
    count = 0
    hotelname = ""
    for j in range(50):
        try:
            final = set_page(hotelid, j + 1)
            hotelname = str([final['hotelName']])
            print("------------------------" + str(j + 1) + "page------------------------" + str(
                len(final['commentList']['comments'])))
        except Exception:
            print("------------------------" + str(j + 1) +
                  "skippage------------------------")
            continue
        # 若發生例外則跳頁執行
        for i in range(len(final['commentList']['comments'])):
            # 排除不需要的語言
            if (final['commentList']['comments'][i]['translateSource'] == 'zh-TW') and (
                    final['commentList']['comments'][i][
                        'translateTarget'] == 'zh-TW'):
                # print("第" + str(count + 1) + "位 " + final['commentList']['comments'][i]['reviewComments'] + "     " +
                #       final['commentList']['comments'][i]['formattedRating'])
                count = count + 1
                checkin = final['commentList']['comments'][i]['checkInDate'][0:10]
                temp2 = pd.DataFrame({'飯店名稱': hotelname,
                                      '距離市中心': str([distance]),
                                      '房客名稱': [str([final['commentList']['comments'][i]['reviewerInfo']['displayMemberName']])],
                                      '房客評論': [str([final['commentList']['comments'][i]['reviewComments']])],
                                      '評分': [str([final['commentList']['comments'][i]['formattedRating']])],
                                      '停留時間': [final['commentList']['comments'][i]['reviewerInfo']['lengthOfStay']],
                                      'checkin': checkin})
                frame = frame.append(temp2, ignore_index=True)
            else:
                continue

        print(count)
    # 按資料date排序
    frame = frame.sort_values(by='checkin', ascending=False)
    frame.reset_index(inplace=True)
    frame = frame.drop(columns=['index'])

    print(str(hotelid) + " " + hotelname + "共" + str(count) + "筆資料")
    hotelnodatacount = hotelnodatacount.append(
        {'飯店名稱': hotelname, '共幾筆評論': str(count)}, ignore_index=True)
    return frame, count, hotelnodatacount


hotelnodatacount = pd.DataFrame(columns=['飯店名稱', '共幾筆評論'])
finalframe = pd.DataFrame(
    columns=['飯店名稱', '距離市中心', '房客名稱', '房客評論', '評分', '停留時間', 'checkin'])
finalcount = 0
print(len(x))
for i in range(20):
    tempmultivalue = hotelinfocrawler(x.iloc[i, 1].item(), x.iloc[i, 2])
    finalcount = finalcount + tempmultivalue[1]
    finalframe = finalframe.append(tempmultivalue[0], ignore_index=True)
    hotelnodatacount = hotelnodatacount.append(
        tempmultivalue[2], ignore_index=True)

print(finalcount)
print(finalframe)
finalframe.to_csv("alltaichungdata_sortbydate.csv", encoding='utf_8_sig')
print(len(hotelnodatacount))
for i in range(len(hotelnodatacount)):
    print(hotelnodatacount.iloc[i, 1])
    if hotelnodatacount.iloc[i, 1] == 0:
        hotelnodatacount.drop([i])
hotelnodatacount.reset_index(inplace=True)
hotelnodatacount = hotelnodatacount.drop(columns=['index'])
hotelnodatacount.to_csv("datacount.csv", encoding='utf_8_sig')
