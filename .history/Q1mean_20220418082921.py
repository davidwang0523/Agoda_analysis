import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import preprocessing
import matplotlib.pyplot as plt
import warnings
import re
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from scipy.spatial.distance import cdist
warnings.filterwarnings('ignore')


def picture(staytime, n):
    staytimetemp = [None]*n
    sum = 0
    for i in range(n):
        staytimetemp[i] = staytime[i]
        sum += staytime[i]
    # plt.figure(figsize=(20, 8))
    # # Simple Exponential Smoothing
        # fit1 = SimpleExpSmoothing(list(reversed(staytimetemp))).fit(
        #     smoothing_level=0.2, optimized=False)
        # yhat = fit1.predict(len(list(reversed(staytimetemp))))
    # print(yhat)
    # # plot
    # l1, = plt.plot(list(fit1.fittedvalues) +
    #                list(fit1.forecast(5)), marker='o')

    # fit2 = SimpleExpSmoothing(list(reversed(staytimetemp))).fit(
    #     smoothing_level=0.6, optimized=False)
    # yhat = fit2.predict(len(list(reversed(staytimetemp))))
    # print(yhat)
    # # plot
    # l2, = plt.plot(list(fit2.fittedvalues) +
    #                list(fit2.forecast(5)), marker='o')

    fit3 = SimpleExpSmoothing(list(reversed(staytimetemp))).fit()
    # plot
    yhat = fit3.predict(len(list(reversed(staytimetemp))))
    # print(yhat)
    # l3, = plt.plot(list(fit3.fittedvalues) +
    #                list(fit3.forecast(5)), marker='o')

    # l4, = plt.plot(list(reversed(staytimetemp)), marker='o')
    # plt.legend(handles=[l1, l2, l3, l4], labels=[
    #     'a=0.2', 'a=0.6', 'auto', 'data'], loc='best', prop={'size': 7})

    print("算術平均數"+str(sum/n))
    # plt.show()
    return yhat


all = pd.DataFrame(columns=['飯店名稱', '平均停留時間', '距離市中心'])
data = pd.read_csv('alltaichungdata_sortbydate.csv')  # 全部資料sort後
datacount = pd.read_csv('datacount.csv')  # 各個飯店名稱以及飯店評論總數

recent = 90  # 設定要幾天
for i in range(len(datacount)):
    temp = ''
    distance = ''
    apprix_1 = data.iloc[:datacount.iloc[i, 2], :]  # 切分dataframe上方
    if len(apprix_1) == 1:  # 只有一筆評價就只用一個評論
        temp = apprix_1.iloc[0, 6]
    elif len(apprix_1) < recent:  # 沒有足夠多的評論就用有的評論做平均
        temp = picture((apprix_1['停留時間']).tolist(), len(apprix_1))
    else:  # 使用設定的評論數量
        temp = picture((apprix_1['停留時間']).tolist(), recent)
    # 對距離使用正則表達式
    num = re.sub(u"([^\u0030-\u0039\u002e\uffe5])",
                 "", str(apprix_1.iloc[0, 2]))
    if num == '':  # 位於市中心 距離設為0
        distance = 0
    else:  # 使用爬蟲到的距離
        distance = num
    all = all.append(
        {'飯店名稱': apprix_1.iloc[0, 1], '平均停留時間': temp, '距離市中心': distance}, ignore_index=True)
    data = data.iloc[datacount.iloc[i, 2]:, :]

print(all)
all.to_csv('kmeans_data.csv', encoding='utf_8_sig')
df = all.drop(columns=['飯店名稱'])

plt.figure(figsize=(10, 8))
plt.xlabel('avgstaytime')
plt.ylabel('distance')
plt.scatter(df['平均停留時間'], df['距離市中心'], c='red', s=50)
plt.title('original data')
plt.savefig('original.jpg')

# 標準化
scaler = preprocessing.MinMaxScaler(feature_range=(0, 1)).fit(df)
processdf = scaler.transform(df)
plt.figure(figsize=(10, 8))
plt.xlabel('avgstaytime')
plt.ylabel('distance')
plt.scatter(processdf[:,0], processdf[:,1], c='red', s=50)
plt.title('minmaxscaler data')
plt.savefig('minmaxscaler.jpg')

# #k means determine k
# distortions = []
# K = range(1, 10)
# for k in K:
#     kmeanModel = KMeans(n_clusters=k).fit(processdf)
#     distortions.append(sum(np.min(cdist(
#         processdf, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / processdf.shape[0])

# # Plot the elbow
# plt.figure(figsize=(10, 8))
# plt.plot(K, distortions, 'bx-')
# plt.xlabel('k')
# plt.ylabel('Distortion')
# plt.title('The Elbow Method showing the optimal k')
# plt.show()

# 分群
kmeans = KMeans(n_clusters=6).fit(df)
# 質心
centroids = kmeans.cluster_centers_
# 視覺化
print(centroids)
plt.figure(figsize=(10, 8))
plt.xlabel('avgstaytime')
plt.ylabel('distance')
plt.scatter(df['平均停留時間'], df['距離市中心'],
            c=kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.title('originalkmeans')
plt.savefig('originalkmeans.jpg')

# 分群
kmeans = KMeans(n_clusters=6).fit(processdf)
# 質心
centroids = kmeans.cluster_centers_
# 視覺化
print(centroids)
plt.figure(figsize=(10, 8))
plt.xlabel('avgstaytime')
plt.ylabel('distance')
plt.scatter(processdf[:, 0], processdf[:, 1],
            c=kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.title('minmaxscalekmeans')
plt.savefig('minmaxscalekmeans.jpg')
