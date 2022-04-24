# webcrawler.py 

# 利用requests套件進行agoda資料爬取
# "taichungframe.csv" 是利用selinium 自動化抓取agoda官網上的台中市飯店id 以及距離市中心的距離
# "alltaichungdata_sortbydate.csv"
# 有進行sortbydate是為了之後抓取最新的評論，此csv是透過 agoda的 hotelreview api requests後即可獲得的資訊（透過taichungframe的hotelid)
# 其中包含 [飯店名稱,距離市中心,房客名稱,房客評論,評分,停留時間,checkin]
# "datacount.csv" 是 每間飯店爬取到的有效評論（其中刪除了沒有評論的飯店）

# main.py
# Q1
# 我們針對'奇異果快捷旅店 - 站前二館 (Kiwi Express Hotel – Taichung Station Branch II)' 探討顧客不滿意此飯店的原因
# 主要使用的套件為snownlp
# 在每個評論使用snownlp之前，先進行評論雜訊處理，例如：評論中含有空白格 /n ....
# 透過snownlp可以為每個評論斷句並且計算他們的正面評價分數，在此處我們將每個斷句的分數加總並除以斷句的數量，便可得知每個評論的評分，輸出為"評論和正面評價分.csv"
# 再利用matplotlib可呈現資料分布的狀況，此處為設定90天，x軸為checkin時間，y軸為分數，(在sentiments.jpg)
# 最後再輸出 "依照負面排序.csv"
# 從情感分析出來的分數來看，我們將小於0.2的當作負評，經由我們統整負面留言的共通點，可以發現主要問題是
# 房間的整潔度、床的舒適度、以及隔音，而我們將大於0.8當作是正面評價，統整正面評價可以發現，這間飯店的優點是交通便利。

# Q2
# 在這邊我們使用的feature為"距離市中心"以及"人氣景點平均距離"，使用的演算法為"kmeans"
# "kmeans_data.csv"的欄位為"飯店名稱,距離市中心,人氣景點平均距離"
# 因為kmeans會受到數值大小的影響，因此我們先對數值部分做了處理，使用的方法為"minmaxscaler"，將數值縮放置[0,1]，圖檔為"minmaxscaler.jpg"
# 之後再進行kmeans choosek 得出的結論為3群，效果可能不錯，圖檔為"choosek.jpg"
# 最後再行kmeans 可得出最後的分群結果 圖檔為"mainmaxscalekmeans.jpg" csv檔案為"minmaxscalekmeans.csv"
# 補充：
# 我們也對沒有做標準化的數據進行了kmeans，檔案為 originalkmeans.jpg以及original.csv
# 發現出來的結果不太符合我們以下的假設：
# 1.距離市中心以及熱門景點都很接近，適合追求都市機能以及熱愛跑景點的旅客
# 2.距離市中心以及熱門景點都不是很近也不是太遠，是另外兩種的混合型，喜歡跑景點但又想體驗渡假村型飯店的遊客
# 3.距離市中心以及熱門景點都相對遙遠，可能是度假村或別墅類型的飯店，適合想在渡假村休假的遊客，想在定點的遊客
# 尤其是上述第3.的data中如果沒有對他們先做標準化得出的數據，會只有4筆資料
# 假如有做標準化會得出16筆資料，並且在閱讀了此類飯店的名稱後，我們認為這個可能比較符合我們一開始的假設。
# 因此最終還是選擇先對資料進行標準化處裡，在進行kmenas分析。


