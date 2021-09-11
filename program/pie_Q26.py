# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 10:51:37 2021

@author: takah
"""

import pandas as pd
import numpy as np
import os 
from matplotlib import pyplot as plt
import japanize_matplotlib
import math
import gc
import collections
os.chdir("D:/documents/夏バイト/Python/program")

main_df=pd.read_csv("../data/JP_MOPS_2020.csv")
add_df=pd.read_csv("../data/ID_産業分類_規模.csv")
df=pd.merge(main_df, add_df,left_on="ID番号",right_on="ID")
df.loc[df["事_従業者数_計"]>=500,"人数分類"]="500人以上"
df.loc[df["事_従業者数_計"]<500,"人数分類"]="250-499人"
df.loc[df["事_従業者数_計"]<250,"人数分類"]="100-249人"
df.loc[df["事_従業者数_計"]<100,"人数分類"]="50-99人"

df.loc[df["Q26_1_1_20_12"]==1,"Q26_1_text"]="導入しておらず、予定もない"
df.loc[df["Q26_1_2_20_12"]==1,"Q26_1_text"]="導入していないが予定がある"
df.loc[df["Q26_1_3_20_12"]==1,"Q26_1_text"]="スタンドアロンをピアツーピアでつないで導入している"
df.loc[df["Q26_1_4_20_12"]==1,"Q26_1_text"]="クライアントサーバーを導入している"
df.loc[df["Q26_1_5_20_12"]==1,"Q26_1_text"]="クラウドを導入している"
df.loc[df["Q26_1_6_20_12"]==1,"Q26_1_text"]="その他"
df["Q26_1_text"]=df["Q26_1_text"].fillna("無回答")

df.loc[df["Q26_2_1_20_12"]==1,"Q26_2_text"]="導入しておらず、予定もない"
df.loc[df["Q26_2_2_20_12"]==1,"Q26_2_text"]="導入していないが予定がある"
df.loc[df["Q26_2_3_20_12"]==1,"Q26_2_text"]="一部の工程に導入している"
df.loc[df["Q26_2_4_20_12"]==1,"Q26_2_text"]="ほとんどの工程に導入している"
df["Q26_2_text"]=df["Q26_2_text"].fillna("無回答")

df.loc[df["Q26_3_1_20_12"]==1,"Q26_3_text"]="導入しておらず、予定もない"
df.loc[df["Q26_3_2_20_12"]==1,"Q26_3_text"]="導入していないが予定がある"
df.loc[df["Q26_3_3_20_12"]==1,"Q26_3_text"]="一部の工程に導入している"
df.loc[df["Q26_3_4_20_12"]==1,"Q26_3_text"]="ほとんどの工程に導入している"
df["Q26_3_text"]=df["Q26_3_text"].fillna("無回答")

n=0
fig=plt.figure(dpi=300)
for i in range(len(df["ID"])):
    a=df.iloc[i,:]
    text_list=df["Q26_1_text"]
    count_Q_26_1=dict(collections.Counter(text_list))
    label=["導入しておらず、予定もない","導入していないが予定がある","スタンドアロンをピアツーピアでつないで導入している","クライアントサーバーを導入している","クラウドを導入している","その他","無回答"]
    label_1=["導入せず、予定もない","導入ないが予定ある","スタンドアロンをピアツーピアでつないで導入","クライアントサーバーを導入","クラウドを導入","その他   ","無回答"]
    lab_i=label.index(a["Q26_1_text"])
    num=[]
    for i in label:
        num.append(count_Q_26_1[i])
    fig.suptitle("IoT利用状況")
    ax=fig.add_subplot(111)
    pie,pie_1=ax.pie(num,startangle=90,labels=label_1,counterclock=False,labeldistance=1.1)
    boxdic = {
        "facecolor" : "white",
        "edgecolor" : "red",
        "boxstyle" : "square",
        "linewidth" : 0.5,
        "alpha" : 1
        }
    
    ax.annotate('',(1.25,1.25), xytext=(pie_1[lab_i]._x*0.7,pie_1[lab_i]._y*0.7),
                        arrowprops=dict(arrowstyle='<|-', 
                                        connectionstyle='arc3', 
                                        facecolor='black', 
                                        edgecolor='black')
                       )
    text="貴事業所の位置"
    ax.text(0.8,1.2,text,bbox=boxdic,size=14)
    file_name="../data/IoT_use_pie/"+str(a["ID"])+"_IoT_use_pie.png"
    fig.savefig(file_name,bbox_inches="tight",dpi=300)
    plt.cla()

    text_list=df["Q26_2_text"]
    count_Q_26_2=dict(collections.Counter(text_list))
    label=["導入しておらず、予定もない","導入していないが予定がある","一部の工程に導入している","ほとんどの工程に導入している","無回答"]
    label_1=["導入せず、予定もない","導入ないが予定ある","一部の工程に導入","ほとんどの工程に導入     ","無回答"]
    lab_i=label.index(a["Q26_2_text"])
    num=[]
    for i in label:
        num.append(count_Q_26_2[i])
    fig.suptitle("AI利用状況")
    ax=fig.add_subplot(111)
    pie,pie_1=ax.pie(num,startangle=90,labels=label_1,counterclock=False,labeldistance=1.1)
    boxdic = {
        "facecolor" : "white",
        "edgecolor" : "red",
        "boxstyle" : "square",
        "linewidth" : 0.5,
        "alpha" : 1
        }
    
    ax.annotate('',(1.25,1.25), xytext=(pie_1[lab_i]._x*0.7,pie_1[lab_i]._y*0.7),
                        arrowprops=dict(arrowstyle='<|-', 
                                        connectionstyle='arc3', 
                                        facecolor='black', 
                                        edgecolor='black')
                       )
    text="貴事業所の位置"
    ax.text(0.8,1.2,text,bbox=boxdic,size=14)
    file_name="../data/AI_use_pie/"+str(a["ID"])+"_AI_use_pie.png"
    fig.savefig(file_name,bbox_inches="tight",dpi=300)
    plt.cla()
    
    text_list=df["Q26_3_text"]
    count_Q_26_3=dict(collections.Counter(text_list))
    label=["導入しておらず、予定もない","導入していないが予定がある","一部の工程に導入している","ほとんどの工程に導入している","無回答"]
    label_1=["導入せず、予定もない","導入ないが予定ある","一部の工程に導入","ほとんどの工程に導入     ","無回答"]
    lab_i=label.index(a["Q26_3_text"])
    num=[]
    for i in label:
        num.append(count_Q_26_3[i])
    fig.suptitle("3D CAD/CAMの利用状況")
    ax=fig.add_subplot(111)
    pie,pie_1=ax.pie(num,startangle=90,labels=label_1,counterclock=False,labeldistance=1.1)
    boxdic = {
            "facecolor" : "white",
        "edgecolor" : "red",
        "boxstyle" : "square",
        "linewidth" : 0.5,
        "alpha" : 1
        }
    
    ax.annotate('',(1.25,1.25), xytext=(pie_1[lab_i]._x*0.7,pie_1[lab_i]._y*0.7),
                        arrowprops=dict(arrowstyle='<|-', 
                                        connectionstyle='arc3', 
                                        facecolor='black', 
                                        edgecolor='black')
                       )
    text="貴事業所の位置"
    ax.text(0.8,1.2,text,bbox=boxdic,size=14)
    file_name="../data/CAD_use_pie/"+str(a["ID"])+"_CAD_use_pie.png"
    fig.savefig(file_name,bbox_inches="tight",dpi=300)
    plt.cla()
    print(n)
    n+=1
