# Ｑ1：利用分類模型來進行顧客飯店推薦 
# Ｑ2：利用sentiment analysis來找出顧客不滿意飯店的原因（我覺得是針對單一飯店）

# step1: check feature
# 能用的特徵（分類模型）multiclassification （監督或是非監督
# maybe use cosinesimiliar???(但偏爛)
# 先想出y = f(X) = w1x1+w2x2+.......+wnxn 
# 飯店端：
# 連續：評論總數 飯店平均評分 
# 非連續：所在城市 
# 客戶端：客戶姓名（也許可當id）飯店評論 飯店評分 入住時間 退房時間 房型 訂房時長 
# 訂房用途："reviewGroupName","roomTypeName"


# 假設要去台中 想去旅遊或是商務 系統推薦旅店
# kmeans 
# 市中心距離 飯店的平均住宿時長（指數平均加權）



