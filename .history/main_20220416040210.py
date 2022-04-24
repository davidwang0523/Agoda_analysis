import pandas as pd
import numpy as np
import sklearn 

# Ｑ1：利用分類模型來進行顧客飯店推薦 
# Ｑ2：利用sentiment analysis來找出顧客不滿意飯店的原因
# step1: check feature
# 能用的特徵（分類模型）multiclassification
# 先想出y=f(X)=w1x1+w2x2+.......+wnxn 
# 目前有的資料欄位 評論總數 所在城市 顧客姓名 
