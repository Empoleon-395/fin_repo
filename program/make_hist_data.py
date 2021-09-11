# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 20:37:07 2021

@author: takah
"""

import pandas as pd
import numpy as np
import os 
from matplotlib import pyplot as plt
import japanize_matplotlib
import math
import gc
os.chdir("D:/documents/夏バイト/Python/program")

main_df=pd.read_csv("../data/JP_MOPS_2020.csv")
add_df=pd.read_csv("../data/ID_産業分類_規模.csv")
df=pd.merge(main_df, add_df,left_on="ID番号",right_on="ID")
df.loc[df["事_従業者数_計"]>=500,"人数分類"]="500人以上"
df.loc[df["事_従業者数_計"]<500,"人数分類"]="250-499人"
df.loc[df["事_従業者数_計"]<250,"人数分類"]="100-249人"
df.loc[df["事_従業者数_計"]<100,"人数分類"]="50-99人"
df.loc[df["事_従業者数_計"]<50,"人数分類"]="30-49人"


df.loc[df['Q24_1_2020_12'] == 1, 'Q24_1_2020_12_score'] = 0
df.loc[df['Q24_1_2020_12'] == 2, 'Q24_1_2020_12_score'] = 0.25
df.loc[df['Q24_1_2020_12'] == 3, 'Q24_1_2020_12_score'] = 0.5
df.loc[df['Q24_1_2020_12'] == 4, 'Q24_1_2020_12_score'] = 0.75
df.loc[df['Q24_1_2020_12'] == 5, 'Q24_1_2020_12_score'] = 1

df.loc[df['Q24_2_2020_12'] == 1, 'Q24_2_2020_12_score'] = 0
df.loc[df['Q24_2_2020_12'] == 2, 'Q24_2_2020_12_score'] = 0.25
df.loc[df['Q24_2_2020_12'] == 3, 'Q24_2_2020_12_score'] = 0.5
df.loc[df['Q24_2_2020_12'] == 4, 'Q24_2_2020_12_score'] = 0.75
df.loc[df['Q24_2_2020_12'] == 5, 'Q24_2_2020_12_score'] = 1

df.loc[df['Q24_3_2020_12'] == 1, 'Q24_3_2020_12_score'] = 0
df.loc[df['Q24_3_2020_12'] == 2, 'Q24_3_2020_12_score'] = 0.25
df.loc[df['Q24_3_2020_12'] == 3, 'Q24_3_2020_12_score'] = 0.5
df.loc[df['Q24_3_2020_12'] == 4, 'Q24_3_2020_12_score'] = 0.75
df.loc[df['Q24_3_2020_12'] == 5, 'Q24_3_2020_12_score'] = 1

df.loc[df['Q24_4_2020_12'] == 1, 'Q24_4_2020_12_score'] = 0
df.loc[df['Q24_4_2020_12'] == 2, 'Q24_4_2020_12_score'] = 0.25
df.loc[df['Q24_4_2020_12'] == 3, 'Q24_4_2020_12_score'] = 0.5
df.loc[df['Q24_4_2020_12'] == 4, 'Q24_4_2020_12_score'] = 0.75
df.loc[df['Q24_4_2020_12'] == 5, 'Q24_4_2020_12_score'] = 1

df.loc[df['Q24_5_2020_12'] == 1, 'Q24_5_2020_12_score'] = 0
df.loc[df['Q24_5_2020_12'] == 2, 'Q24_5_2020_12_score'] = 0.25
df.loc[df['Q24_5_2020_12'] == 3, 'Q24_5_2020_12_score'] = 0.5
df.loc[df['Q24_5_2020_12'] == 4, 'Q24_5_2020_12_score'] = 0.75
df.loc[df['Q24_5_2020_12'] == 5, 'Q24_5_2020_12_score'] = 1

df.loc[df['Q24_6_2020_12'] == 1, 'Q24_6_2020_12_score'] = 0
df.loc[df['Q24_6_2020_12'] == 2, 'Q24_6_2020_12_score'] = 0.25
df.loc[df['Q24_6_2020_12'] == 3, 'Q24_6_2020_12_score'] = 0.5
df.loc[df['Q24_6_2020_12'] == 4, 'Q24_6_2020_12_score'] = 0.75
df.loc[df['Q24_6_2020_12'] == 5, 'Q24_6_2020_12_score'] = 1

df["Q24_2020_12_ave"]=np.nan

temp_bool=np.sum(np.isnan(df.loc[:,"Q24_1_2020_12_score":"Q24_6_2020_12_score"]),axis=1)

for i,b in enumerate(temp_bool):
    if b <=3:
        df["Q24_2020_12_ave"][i]=np.nanmean(df.loc[:,"Q24_1_2020_12_score":"Q24_6_2020_12_score"].iloc[i,:])

df.loc[df['Q24_1_2015'] == 1, 'Q24_1_2015_score'] = 0
df.loc[df['Q24_1_2015'] == 2, 'Q24_1_2015_score'] = 0.25
df.loc[df['Q24_1_2015'] == 3, 'Q24_1_2015_score'] = 0.5
df.loc[df['Q24_1_2015'] == 4, 'Q24_1_2015_score'] = 0.75
df.loc[df['Q24_1_2015'] == 5, 'Q24_1_2015_score'] = 1

df.loc[df['Q24_2_2015'] == 1, 'Q24_2_2015_score'] = 0
df.loc[df['Q24_2_2015'] == 2, 'Q24_2_2015_score'] = 0.25
df.loc[df['Q24_2_2015'] == 3, 'Q24_2_2015_score'] = 0.5
df.loc[df['Q24_2_2015'] == 4, 'Q24_2_2015_score'] = 0.75
df.loc[df['Q24_2_2015'] == 5, 'Q24_2_2015_score'] = 1

df.loc[df['Q24_3_2015'] == 1, 'Q24_3_2015_score'] = 0
df.loc[df['Q24_3_2015'] == 2, 'Q24_3_2015_score'] = 0.25
df.loc[df['Q24_3_2015'] == 3, 'Q24_3_2015_score'] = 0.5
df.loc[df['Q24_3_2015'] == 4, 'Q24_3_2015_score'] = 0.75
df.loc[df['Q24_3_2015'] == 5, 'Q24_3_2015_score'] = 1

df.loc[df['Q24_4_2015'] == 1, 'Q24_4_2015_score'] = 0
df.loc[df['Q24_4_2015'] == 2, 'Q24_4_2015_score'] = 0.25
df.loc[df['Q24_4_2015'] == 3, 'Q24_4_2015_score'] = 0.5
df.loc[df['Q24_4_2015'] == 4, 'Q24_4_2015_score'] = 0.75
df.loc[df['Q24_4_2015'] == 5, 'Q24_4_2015_score'] = 1

df.loc[df['Q24_5_2015'] == 1, 'Q24_5_2015_score'] = 0
df.loc[df['Q24_5_2015'] == 2, 'Q24_5_2015_score'] = 0.25
df.loc[df['Q24_5_2015'] == 3, 'Q24_5_2015_score'] = 0.5
df.loc[df['Q24_5_2015'] == 4, 'Q24_5_2015_score'] = 0.75
df.loc[df['Q24_5_2015'] == 5, 'Q24_5_2015_score'] = 1

df.loc[df['Q24_6_2015'] == 1, 'Q24_6_2015_score'] = 0
df.loc[df['Q24_6_2015'] == 2, 'Q24_6_2015_score'] = 0.25
df.loc[df['Q24_6_2015'] == 3, 'Q24_6_2015_score'] = 0.5
df.loc[df['Q24_6_2015'] == 4, 'Q24_6_2015_score'] = 0.75
df.loc[df['Q24_6_2015'] == 5, 'Q24_6_2015_score'] = 1

df["Q24_2015_ave"]=np.nan

temp_bool=np.sum(np.isnan(df.loc[:,"Q24_1_2015_score":"Q24_6_2015_score"]),axis=1)

for i,b in enumerate(temp_bool):
    if b <=3:
        df["Q24_2015_ave"][i]=np.nanmean(df.loc[:,"Q24_1_2015_score":"Q24_6_2015_score"].iloc[i,:])


fig=plt.figure(figsize=(18,6))
for i in range(len(df["ID"])):
    list_temp=df.iloc[i,:]
    
    a=list_temp["Q24_2015_ave"]
    
    ax = fig.add_subplot(1,2,1)
    ax.set_xlim(-0.025,1.025)
    ax.set_ylim(0,950)
    edges=[i*0.01 for i in list(range(0,100,5))]
    n, bins, patches = ax.hist(df["Q24_2015_ave"], bins=edges,ec="black",color=["cyan"])
    ax.set_title('2015年度:データ分析活用スコアの分布')
    ax.set_xlabel('スコア')
    ax.set_ylabel('頻度')
    if np.isnan(a)==False:
        u=u=sorted(df["Q24_2015_ave"], key=lambda x: np.inf if np.isnan(x) else x)
        u_2=[x for x in u if math.isnan(x) == False]
        u_2.index(a)
        p=np.round(100-(u.index(a)/len(u_2)*100),decimals=2)
        
        if a<0.05:
            patch=0
            box_x=0
            start=(0.1,595)
            end=(0.015,50)
        elif a<0.1:
            patch=1
            box_x=0
            end=(0.065,50)
            start=(0.1,595)
        elif a<0.15:
            patch=2
            box_x=0
            end=(0.115,50)
            start=(0.1,595)
        elif a<0.2:
            patch=3
            box_x=0
            end=(0.165,50)
            start=(0.1,595)
        elif a<0.25:
            patch=4
            box_x=0
            end=(0.215,50)
            start=(0.1,595)
        elif a<0.3:
            patch=5
            box_x=0
            end=(0.265,180)
            start=(0.1,595)
        elif a<0.35:
            patch=6
            box_x=0
            end=(0.315,180)
            start=(0.1,595)
        elif a<0.4:
            patch=7
            box_x=0
            end=(0.365,180)
            start=(0.1,595)
        elif a<0.45:
            patch=8
            box_x=0
            end=(0.415,180)
            start=(0.1,595)
        elif a<0.5:
            patch=9
            box_x=0
            end=(0.465,180)
            start=(0.1,595)
        elif a<0.55:
            patch=10
            box_x=0.75
            start=(0.85,595)
            end=(0.515,400)
        elif a<0.6:
            patch=11
            box_x=0.75
            start=(0.85,595)
            end=(0.565,180)
        elif a<0.65:
            patch=12
            box_x=0.75
            start=(0.85,595)
            end=(0.615,180)
        elif a<0.7:
            box_x=0.75
            patch=13
            start=(0.85,595)
            end=(0.665,180)
        elif a<0.75:
            patch=14
            box_x=0.75
            start=(0.85,595)
            end=(0.715,180)
        elif a<0.8:
            patch=15
            box_x=0.75
            start=(0.85,595)
            end=(0.765,50)
        elif a<0.85:
            patch=16
            box_x=0.75
            start=(0.85,595)
            end=(0.815,30)
        elif a<0.9:
            patch=17
            box_x=0.75
            start=(0.85,595)
            end=(0.865,30)
        elif a<0.95:
            patch=18
            box_x=0.75
            start=(0.85,595)
            end=(0.915,30)
        else:
            patch=19
            box_x=0.75
            start=(0.85,595)
            end=(0.965,30)
    
    
        boxdic = {
            "facecolor" : "white",
            "edgecolor" : "red",
            "boxstyle" : "square",
            "linewidth" : 0.5,
            "alpha" : 1
            }
        ax.annotate('', start, xytext=end,
                    arrowprops=dict(arrowstyle='<|-', 
                                    connectionstyle='arc3', 
                                    facecolor='black', 
                                    edgecolor='black')
                   )
        
        text="貴事業所の位置\nスコア:"+str(np.round(a,decimals=4))+"点\n上位"+str(p)+"%"
        ax.text(box_x,600,text,bbox=boxdic,size=18)
        try:
            patches[patch].set_facecolor('red')
        except:
            print(a)
    
    a=list_temp["Q24_2020_12_ave"]
    ax1 = fig.add_subplot(1,2,2)
    ax1.set_xlim(-0.025,1.025)
    ax1.set_ylim(0,950)
    edges=[i*0.01 for i in list(range(0,100,5))]
    n, bins, patches = ax1.hist(df["Q24_2020_12_ave"], bins=edges,ec="black",color=["cyan"])
    ax1.set_title('2020年度:データ分析活用スコアの分布')
    ax1.set_xlabel('スコア')
    ax1.set_ylabel('頻度')
    if np.isnan(a)==False:
        u=sorted(df["Q24_2020_12_ave"], key=lambda x: np.inf if np.isnan(x) else x)
        u_2=[x for x in u if math.isnan(x) == False]
        u_2.index(a)
        p=np.round(100-(u.index(a)/len(u_2)*100),decimals=2)
        
        if a<0.05:
            patch=0
            box_x=0
            start=(0.1,595)
            end=(0.015,50)
        elif a<0.1:
            patch=1
            box_x=0
            end=(0.065,50)
            start=(0.1,595)
        elif a<0.15:
            patch=2
            box_x=0
            end=(0.115,50)
            start=(0.1,595)
        elif a<0.2:
            patch=3
            box_x=0
            end=(0.165,50)
            start=(0.1,595)
        elif a<0.25:
            patch=4
            box_x=0
            end=(0.215,50)
            start=(0.1,595)
        elif a<0.3:
            patch=5
            box_x=0
            end=(0.265,180)
            start=(0.1,595)
        elif a<0.35:
            patch=6
            box_x=0
            end=(0.315,180)
            start=(0.1,595)
        elif a<0.4:
            patch=7
            box_x=0
            end=(0.365,180)
            start=(0.1,595)
        elif a<0.45:
            patch=8
            box_x=0
            end=(0.415,180)
            start=(0.1,595)
        elif a<0.5:
            patch=9
            box_x=0
            end=(0.465,180)
            start=(0.1,595)
        elif a<0.55:
            patch=10
            box_x=0.75
            start=(0.85,595)
            end=(0.515,400)
        elif a<0.6:
            patch=11
            box_x=0.75
            start=(0.85,595)
            end=(0.565,180)
        elif a<0.65:
            patch=12
            box_x=0.75
            start=(0.85,595)
            end=(0.615,180)
        elif a<0.7:
            box_x=0.75
            patch=13
            start=(0.85,595)
            end=(0.665,180)
        elif a<0.75:
            patch=14
            box_x=0.75
            start=(0.85,595)
            end=(0.715,180)
        elif a<0.8:
            patch=15
            box_x=0.75
            start=(0.85,595)
            end=(0.765,50)
        elif a<0.85:
            patch=16
            box_x=0.75
            start=(0.85,595)
            end=(0.815,30)
        elif a<0.9:
            patch=17
            box_x=0.75
            start=(0.85,595)
            end=(0.865,30)
        elif a<0.95:
            patch=18
            box_x=0.75
            start=(0.85,595)
            end=(0.915,30)
        else:
            patch=19
            box_x=0.75
            start=(0.85,595)
            end=(0.965,30)
    
    
        boxdic = {
            "facecolor" : "white",
            "edgecolor" : "red",
            "boxstyle" : "square",
            "linewidth" : 0.5,
            "alpha" : 1
            }
        ax1.annotate('', start, xytext=end,
                    arrowprops=dict(arrowstyle='<|-', 
                                    connectionstyle='arc3', 
                                    facecolor='black', 
                                    edgecolor='black')
                   )
        
        text="貴事業所の位置\nスコア:"+str(np.round(a,decimals=4))+"点\n上位"+str(p)+"%"
        ax1.text(box_x,600,text,bbox=boxdic,size=18)
        try:
            patches[patch].set_facecolor('red')
        except:
            print(a)
    
    file_name="../data/data_use_hist/"+str(list_temp["ID"])+"_data_use_hist.png"

    fig.savefig(file_name,bbox_inches='tight',dpi=300)
    plt.cla()
    ax=fig.add_subplot(121)
    plt.cla()


n=0
fig = plt.figure(figsize=(6,0.5))
for i in range(len(df["ID"])):
    list_temp=df.iloc[i,:]
    score_list_temp=list(df[(df["事_産業中分類_内容"]==list_temp["事_産業中分類_内容"])&(df["人数分類"]==list_temp["人数分類"])]["Q24_2020_12_ave"])
    u=sorted(score_list_temp, key=lambda x: np.inf if np.isnan(x) else x)
    u_2=[x for x in u if math.isnan(x) == False]
    temp_mean=np.nanmean(score_list_temp)
    if np.isnan(list_temp["Q24_2020_12_ave"])==False:
        p=np.round(100-(u_2.index(list_temp["Q24_2020_12_ave"])/len(u_2)*100),2)
        p_text=str(np.round(list_temp["Q24_2020_12_ave"],2))+"(上位"+str(p)+"%)"
    else:
        p_text="算出不可"
    
    table_list=[[list_temp["事_産業中分類_内容"],list_temp["人数分類"],str(np.round(temp_mean,2)),p_text]]

    ax1 = fig.add_subplot(111)
    ax1.table(cellText=table_list,colLabels=["産業","規模","産業と規模別の平均","貴事業所のスコア"],rowLabels=[list_temp["HC"]], loc="center")
    ax1.axis('tight')
    ax1.axis('off')
    ax1.grid('off')
    file_name="../data/data_use_table/"+str(list_temp["ID"])+"_data_use_table.png"
    fig.savefig(file_name,bbox_inches="tight",dpi=300)
    plt.cla()
    print(n)
    n+=1










