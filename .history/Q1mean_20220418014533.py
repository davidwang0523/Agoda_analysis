# 目前只有飯店一
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import warnings
import re
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing, Holt
warnings.filterwarnings('ignore')


def picture(staytime, n):
    staytimetemp = [None]*n
    sum = 0
    for i in range(n):
        staytimetemp[i] = staytime[i]
        sum += staytime[i]
    # plt.figure(figsize=(20, 8))
    # # Simple Exponential Smoothing
    fit1 = SimpleExpSmoothing(list(reversed(staytimetemp))).fit(
        smoothing_level=0.2, optimized=False)
    yhat = fit1.predict(len(list(reversed(staytimetemp))))
    #print(yhat)
    # # plot
    # l1, = plt.plot(list(fit1.fittedvalues) +
    #                list(fit1.forecast(5)), marker='o')

    fit2 = SimpleExpSmoothing(list(reversed(staytimetemp))).fit(
        smoothing_level=0.6, optimized=False)
    yhat = fit2.predict(len(list(reversed(staytimetemp))))
    #print(yhat)
    # # plot
    # l2, = plt.plot(list(fit2.fittedvalues) +
    #                list(fit2.forecast(5)), marker='o')

    fit3 = SimpleExpSmoothing(list(reversed(staytimetemp))).fit()
    # plot
    yhat = fit3.predict(len(list(reversed(staytimetemp))))
    #print(yhat)
    # l3, = plt.plot(list(fit3.fittedvalues) +
    #                list(fit3.forecast(5)), marker='o')

    # l4, = plt.plot(list(reversed(staytimetemp)), marker='o')
    # plt.legend(handles=[l1, l2, l3, l4], labels=[
    #     'a=0.2', 'a=0.6', 'auto', 'data'], loc='best', prop={'size': 7})
    print("算術平均數"+str(sum/n))
    # plt.show()
    return sum/n


all = pd.DataFrame(columns=['飯店名稱', '平均停留時間','距離市中心'])
data = pd.read_csv('alltaichungdata_sortbydate.csv')  # 全部資料sort後
datacount = pd.read_csv('datacount.csv')  # 各個飯店的count
recent = 300  # 設定要幾天
for i in range(len(datacount)): # 沒有重複的id 且沒有評論等於0的飯店資料
    temp = ''
    distance=''
    apprix_1 = data.iloc[:datacount.iloc[i, 2], :]  # 切分出上方
    if len(apprix_1) == 1:  # 假設只有一筆評價
        temp = apprix_1.iloc[0,6]
    elif len(apprix_1) < recent:  # 沒有足夠多的評論
        print(apprix_1.iloc[0, 1])
        temp = picture((apprix_1['停留時間']).tolist(), len(apprix_1))
    else:
        print(apprix_1.iloc[0, 1])
        temp = picture((apprix_1['停留時間']).tolist(), recent)
    
    num = re.sub(u"([^\u0030-\u0039\u002e\uffe5])",
                 "", str(apprix_1.iloc[0, 2]))
    if num == '':
        distance=0
    else:
        distance=num
    all = all.append(
        {'飯店名稱': apprix_1.iloc[0, 1], '平均停留時間': temp,'距離市中心':distance}, ignore_index=True)
    data = data.iloc[datacount.iloc[i, 2]:, :]

print(all)
all.to_csv('kmeans_data.csv',encoding='utf_8_sig')

