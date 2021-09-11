# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 17:08:07 2021

@author: takah
"""

import pandas as pd
import numpy as np
import os
###ワーキングディレクトリの設定
os.chdir("C:/Users/takah/Dropbox/My PC (DESKTOP-4MU76QI)/Desktop/卒論用/program")
from my_semi_ml import my_semi_ml
from my_doc2vec import my_doc2vec
from my_plot import my_plot


###torikizokuの分析
##データ読み込み
df_raw=pd.read_csv("../data/torikizoku_twitter.csv")
df_wakati=pd.read_csv("../data/toriki_wakati.csv")

##doc2vec
d2v=my_doc2vec()
d2v.fit(df_wakati)
df_vec=d2v.return_df()

##半教師あり学習
initial_t=[1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,1,0,1,0,0,0,0,1,1,0,1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,1,0,1,1,0,1,1,0,0,1,0,1,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,1,1,0,0,1]
sm=my_semi_ml()
sm.fit(df=df_vec,initial_t=initial_t)

df_teacher, df_teacher_g, df_teacher_b = sm.return_df(df_wakati)
df_teacher_raw, df_teacher_g_raw, df_teacher_b_raw = sm.return_df(df_raw)

##プロット
pplot = my_plot(df_teacher)
pplot.time_plot("../data/test_plot")
pplot.season_pie("../data/test_pie")

##好印象、悪印象それぞれ分析
d2v_g = my_doc2vec()
d2v_b = my_doc2vec()
d2v_g.fit(df_teacher_g)
d2v_b.fit(df_teacher_b)

d2v_g.similar_words("行く",50)
d2v_b.similar_words("行く",50)
