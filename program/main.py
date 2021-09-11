##パッケージのインポート
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.svm import SVC

##データの読み込み
train_x=pd.read_csv("../data/train.csv")
test_x=pd.read_csv("../data/test.csv")
answer=pd.read_csv("../data/ans.csv")
train_x=


##
