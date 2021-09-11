# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 14:17:24 2021

@author: takah
"""

import pandas as pd
import numpy as np
import os
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import datetime
import japanize_matplotlib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import lightgbm as lgb
import collections
from gensim.models import word2vec
from janome.tokenizer import Tokenizer


os.chdir("C:/Users/takah/Dropbox/My PC (DESKTOP-4MU76QI)/Desktop/卒論用/program")
df_raw=pd.read_csv("../data/torikizoku_twitter.csv")
df=pd.read_csv("../data/toriki_wakati.csv")

###再現性
os.environ['PYTHONHASHSEED']="0"

###doc2vecの実行
class doc_2_vbec:
        
    def fit(self,df,size=100):
        self.df=df
        self.word_list=df["tweet"]
        self.vec_list=[]
        self.tag_list = [TaggedDocument(words=eval(doc), tags=[i]) for i, doc in enumerate(self.word_list)]
        self.model=Doc2Vec(documents=self.tag_list,vector_size=size, window=5, min_count=5, workers=4,seed=0)
        for i in range(len(self.word_list)):
            self.vec_list.append(list(self.model.dv.get_vector(i)))
        self.df_2=pd.DataFrame({"date":self.df["date"],
                                "ID":self.df["ID"],
                                "tweet":self.vec_list})        
        
    def retrun_df(self):
        return self.df_2
    
    def similar_words(self,word,num=10):
        ret = self.model.wv.most_similar(positive=[word],topn=num) 
        for item in ret:
            print(item[0], item[1])
    
    def similar_2words(self,word1,word2,num=10):
        ret = self.model.wv.most_similar(positive=[word1,word2],topn=num) 
        for item in ret:
            print(item[0], item[1])

a=doc_2_vbec(df, 100)
df_vec=a.df_2
a_doc=a.tag_list
a.model.wv.most_similar(positive=["行く"])

###半教師あり学習の実装
def croval_rf(df):
    train_y=df["teacher"]
    train_x=df.drop("teacher",axis=1)
    best_cross_val_score=0
    
    for n in [1,2,5,10,20,50,100,200]:
        for d in [1,2,5,10,20,50]:
            clf=RandomForestClassifier(n_estimators=n,max_depth=d,random_state=0)
            clf.fit(train_x,train_y)
            cv_score=np.mean(cross_val_score(clf,train_x,train_y))
            if best_cross_val_score<cv_score:
                best_val_param=[n,d]
                best_clf=clf
                best_cross_val_score=cv_score
    return best_clf,best_cross_val_score,best_val_param

def hold_rf(df):
    train_x_y ,test_x_y=train_test_split(df)
    train_y=train_x_y["teacher"]
    train_x=train_x_y.drop("teacher",axis=1)
    test_y=test_x_y["teacher"]
    test_x=test_x_y.drop("teacher",axis=1)
    best_acc_score=0
    for n in [1,2,5,10,20,50,100,200]:
        for d in [1,2,5,10,20,50]:
            clf=RandomForestClassifier(n_estimators=n,max_depth=d,random_state=0)
            clf.fit(train_x,train_y)
            pred_y=clf.predict(test_x)
            acc_score=accuracy_score(test_y, pred_y)
            if best_acc_score<acc_score:
                best_acc_score=acc_score
                best_clf=clf
                best_val_param=[n,d]
    return best_clf,best_acc_score,best_val_param

a=doc_2_vbec(df, 100)
df_vec=a.df_2
teacher_list=[np.nan]*len(df_vec)
initial_t=[1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,1,0,1,0,0,0,0,1,1,0,1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,1,0,1,1,0,1,1,0,0,1,0,1,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,1,1,0,0,1]

teacher_list[0:len(initial_t)]=initial_t

y_data=[i for i in teacher_list if np.isnan(i)==False]
x_data=[df_vec["tweet"][i] for i in range(len(teacher_list)) if np.isnan(teacher_list[i])==False]
x_df=pd.DataFrame(x_data)
x_y_df=pd.merge(x_df,pd.DataFrame({"teacher":y_data}),left_index=True,right_index=True)
pd.DataFrame({"teacher":y_data})
while True:
    n=0
    
    y_data=[i for i in teacher_list if np.isnan(i)==False]
    x_data=[df_vec["tweet"][i] for i in range(len(teacher_list)) if np.isnan(teacher_list[i])==False]
    x_df=pd.DataFrame(x_data)
    x_y_df=pd.merge(x_df,pd.DataFrame({"teacher":y_data}),left_index=True,right_index=True)
    pd.DataFrame({"teacher":y_data})
    
    if len(x_y_df)<1000:
        bm,bs,bp=croval_rf(x_y_df)
    else:
        bm,bs,bp=hold_rf(x_y_df)
    
    new_teacher=bm.predict_proba(pd.DataFrame(list(df_vec["tweet"])))

    if sum(np.isnan(teacher_list))==0:
        print("全てに教師データがついたため停止しました。")
        break
    
    for i in range(len(teacher_list)):
        if np.isnan(teacher_list[i]):
            if new_teacher[:,1][i]>=0.8:
                teacher_list[i]=1
                print("add 1 in ",i)
                n=1
            elif new_teacher[:,1][i]<=0.2:
                teacher_list[i]=0
                n=1
    
    if n==0:
        print("教師データがこれ以上増えないため停止します。")
        break
    else:
        nn=sum(np.isnan(teacher_list))
        print("残り : ",nn)

df_teacher=df_raw.merge(pd.DataFrame({"teacher":teacher_list}),left_index=True,right_index=True)
df_teacher.to_csv("../data/torikizoku_teacher.csv")
df=df.merge(pd.DataFrame({"teacher":teacher_list}),left_index=True,right_index=True)

###時期ごとのデータフレーム
df_season1=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")<datetime.datetime(2020,4,7)])
df_season2=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime(2020,4,7)<=datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")<datetime.datetime(2020,5,25)])
df_season3=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime(2020,5,25)<=datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")<datetime.datetime(2021,1,7)])
df_season4=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime(2021,1,7)<=datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")<datetime.datetime(2021,3,18)])
df_season5=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime(2021,3,18)<=datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")<datetime.datetime(2021,4,23)])
df_season6=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime(2021,4,23)<=datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")<datetime.datetime(2021,6,21)])
df_season7=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime(2021,6,21)<=datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")])

###ツイート数の推移
tweet_num_list=[len(df_season1),len(df_season2),len(df_season3),len(df_season4),len(df_season5),len(df_season6),len(df_season7)]
fig=plt.figure(dpi=300)
ax1=fig.add_subplot(111)
ax1.plot(tweet_num_list)
ax1.set_xticklabels(["","コロナ前","1回緊急事態宣言","GoToキャンペーン等","2回緊急事態宣言","蔓延防止法","3回緊急事態宣言","宣言解除後"],rotation=90)
fig.show()

###１，０，NAの時期ごとの割合
fig=plt.figure(dpi=300)

pie_list_label=["0","1","NA"]

ax1=fig.add_subplot(241)
pie_list_value=(collections.Counter(df_teacher["teacher"].fillna("NA")))
pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
ax1.set_title("全体の比率")
ax1.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)

ax2=fig.add_subplot(242)
pie_list_value=(collections.Counter(df_season1["teacher"].fillna("NA")))
pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
ax2.set_title("コロナ前")
ax2.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)

ax3=fig.add_subplot(243)
pie_list_value=(collections.Counter(df_season2["teacher"].fillna("NA")))
pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
ax3.set_title("1回緊急事態宣言")
ax3.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)

ax4=fig.add_subplot(244)
pie_list_value=(collections.Counter(df_season3["teacher"].fillna("NA")))
pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
ax4.set_title("GoTo")
ax4.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)

ax5=fig.add_subplot(245)
pie_list_value=(collections.Counter(df_season4["teacher"].fillna("NA")))
pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
ax5.set_title("2回緊急事態宣言")
ax5.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)

ax6=fig.add_subplot(246)
pie_list_value=(collections.Counter(df_season5["teacher"].fillna("NA")))
pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
ax6.set_title("蔓延防止法")
ax6.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)

ax7=fig.add_subplot(247)
pie_list_value=(collections.Counter(df_season6["teacher"].fillna("NA")))
pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
ax7.set_title("3回緊急事態宣言")
ax7.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)

ax8=fig.add_subplot(248)
pie_list_value=(collections.Counter(df_season7["teacher"].fillna("NA")))
pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
ax8.set_title("宣言解除後")
ax8.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)

fig.show()

df_good=df[df["teacher"]==1]

df_bad=df[df["teacher"]==0]

b=doc_2_vbec()
b.fit(df_good,size=100)
b.similar_words("行く",100)



