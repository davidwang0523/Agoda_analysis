# 目前只有飯店一
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import warnings
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing, Holt
warnings.filterwarnings('ignore')

data = pd.read_csv('alltaichungdata_sortbydate.csv')  # 全部資料sort後
datacount = pd.read_csv('datacount.csv')  # 各個飯店的count
for i in range(len(datacount)):
    apprix_1 = data.iloc[:datacount.iloc[i,1],:]
    print(apprix_1.head())

# def picture(staytime, n):
#     staytimetemp = [None]*n
#     sum = 0
#     for i in range(n):
#         staytimetemp[i] = staytime[i]
#         sum += staytime[i]
#     # plt.figure(figsize=(20, 8))
#     # # Simple Exponential Smoothing
#     # fit1 = SimpleExpSmoothing(list(reversed(staytimetemp))).fit(
#     #     smoothing_level=0.2, optimized=False)
#     # yhat = fit1.predict(len(list(reversed(staytimetemp))))
#     # print(yhat)
#     # # plot
#     # l1, = plt.plot(list(fit1.fittedvalues) +
#     #                list(fit1.forecast(5)), marker='o')

#     # fit2 = SimpleExpSmoothing(list(reversed(staytimetemp))).fit(
#     #     smoothing_level=0.6, optimized=False)
#     # yhat = fit2.predict(len(list(reversed(staytimetemp))))
#     # print(yhat)
#     # # plot
#     # l2, = plt.plot(list(fit2.fittedvalues) +
#     #                list(fit2.forecast(5)), marker='o')

#     # fit3 = SimpleExpSmoothing(list(reversed(staytimetemp))).fit()
#     # # plot
#     # yhat = fit3.predict(len(list(reversed(staytimetemp))))
#     # print(yhat)
#     # l3, = plt.plot(list(fit3.fittedvalues) +
#     #                list(fit3.forecast(5)), marker='o')

#     # l4, = plt.plot(list(reversed(staytimetemp)), marker='o')
#     # plt.legend(handles=[l1, l2, l3, l4], labels=[
#     #     'a=0.2', 'a=0.6', 'auto', 'data'], loc='best', prop={'size': 7})
#     print("算術平均數"+str(sum/n))
#     # plt.show()


# picture(staytime, 90)
