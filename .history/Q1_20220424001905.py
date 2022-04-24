import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import preprocessing
import matplotlib.pyplot as plt
import warnings
import re
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from scipy.spatial.distance import cdist
from snownlp import SnowNLP
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


all = pd.DataFrame(columns=['飯店名稱', '平均停留時間', '距離市中心', '人氣景點平均距離'])
data = pd.read_csv('alltaichungdata_sortbydate.csv')  # 全部資料sort後
datacount = pd.read_csv('datacount.csv')  # 各個飯店名稱以及飯店評論總數

recent = 90  # 設定要幾天
for i in range(len(datacount)):
    temp = ''
    distance = ''
    apprix_1 = data.iloc[:datacount.iloc[i, 2], :]  # 切分dataframe上方
    data = data.iloc[datacount.iloc[i, 2]:, :]
    # 平均值計算
    if len(apprix_1) == 1:  # 只有一筆評價就只用一個評論
        temp = apprix_1.iloc[0, 6]
    elif len(apprix_1) < recent:  # 沒有足夠多的評論就用有的評論做平均
        temp = picture((apprix_1['停留時間']).tolist(), len(apprix_1))
    else:  # 使用設定的評論數量
        temp = picture((apprix_1['停留時間']).tolist(), recent)

    # 對distance使用正則表達式
    if str(apprix_1.iloc[0, 2]).find('位於市中心') != -1:
        distance = 0
    elif str(apprix_1.iloc[0, 2]).find('查看地圖') != -1:
        print(apprix_1.iloc[0, 1])
        continue
    else:  # 使用爬蟲到的距離
        num = re.sub(u"([^\u0030-\u0039\u002e\uffe5])",
                     "", str(apprix_1.iloc[0, 2]))
        distance = num
    all = all.append(
        {'飯店名稱': apprix_1.iloc[0, 1], '平均停留時間': temp, '距離市中心': distance, '人氣景點平均距離': datacount.iloc[i, 3]}, ignore_index=True)

 # 最後選擇使用 距離市中心 以及人氣景點平均距離作為分析
 # 原數據
annotations = all['飯店名稱'].to_list()
all.to_csv('kmeans_data.csv', encoding='utf_8_sig')
df = all.drop(columns=['飯店名稱'])
df = df.drop(columns=['平均停留時間'])
plt.figure(figsize=(10, 8))
plt.xlabel('distanceofcitycenter')
plt.ylabel('hot spot')
plt.scatter(df['距離市中心'], df['人氣景點平均距離'], c='red', s=50)
plt.title('original data')
plt.savefig('original.jpg')

# 標準化
scaler = preprocessing.MinMaxScaler(feature_range=(0, 1)).fit(df)
processdf = scaler.transform(df)
plt.figure(figsize=(10, 8))
plt.xlabel('distanceofcitycenter')
plt.ylabel('hot spot')
plt.scatter(processdf[:, 0], processdf[:, 1], c='red', s=50)
plt.title('minmaxscaler data')
plt.savefig('minmaxscaler.jpg')


# k means determine k
distortions = []
K = range(1, 10)
for k in K:
    kmeanModel = KMeans(n_clusters=k).fit(processdf)
    distortions.append(sum(np.min(cdist(
        processdf, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / processdf.shape[0])
# Plot
plt.figure(figsize=(10, 8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.savefig('choosek.jpg')


# 分群
kmeans = KMeans(n_clusters=3).fit(df)
# 質心
centroids = kmeans.cluster_centers_
# 視覺化
# print(centroids)
originalkmeans = pd.DataFrame(columns=['飯店名稱', '分群'])
for i in range(len(annotations)):
    originalkmeans = originalkmeans.append(
        {'飯店名稱': annotations[i], '分群': '第'+str(kmeans.labels_[i])+'群'}, ignore_index=True)
originalkmeans.to_csv('originkmeans.csv', encoding='utf_8_sig')
plt.figure(figsize=(10, 8))
plt.xlabel('distanceofcitycenter')
plt.ylabel('hot spot')
plt.scatter(df['距離市中心'], df['人氣景點平均距離'],
            c=kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.title('originalkmeans')
plt.savefig('originalkmeans.jpg')


# 分群
kmeans2 = KMeans(n_clusters=3).fit(processdf)
# 質心
centroids = kmeans2.cluster_centers_
# 視覺化
# print(centroids)
minmaxscalekmeans = pd.DataFrame(columns=['飯店名稱', '分群'])
for i in range(len(annotations)):
    minmaxscalekmeans = minmaxscalekmeans.append(
        {'飯店名稱': annotations[i], '分群': '第'+str(kmeans2.labels_[i])+'群'}, ignore_index=True)
minmaxscalekmeans.to_csv('minmaxscalekmeans.csv', encoding='utf_8_sig')
plt.figure(figsize=(10, 8))
plt.xlabel('distanceofcitycenter')
plt.ylabel('hot spot')
plt.scatter(processdf[:, 0], processdf[:, 1],
            c=kmeans2.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.title('minmaxscalekmeans')
plt.savefig('minmaxscalekmeans.jpg')

# Q2
comment = pd.read_csv('alltaichungdata_sortbydate.csv')
print(comment.head())
x = (comment['房客評論'].iloc[:1000]).tolist()
print(x[2])
s = SnowNLP(x[2])
for i in range(20):
    try:
     s1=SnowNLP(s.sentiments[i])
     print(s1.sentiments)
    except Exception:
        break
print(s.sentiments)

