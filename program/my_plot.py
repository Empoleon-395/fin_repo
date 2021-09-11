# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 17:12:52 2021

@author: takah
"""
import datetime
import pandas as pd
from matplotlib import pyplot as plt
import collections

class my_plot:
    def __init__(self,df):
        ###時期ごとのデータフレーム
        self.df=df
        self.df_season1=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")<datetime.datetime(2020,4,7)])
        self.df_season2=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime(2020,4,7)<=datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")<datetime.datetime(2020,5,25)])
        self.df_season3=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime(2020,5,25)<=datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")<datetime.datetime(2021,1,7)])
        self.df_season4=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime(2021,1,7)<=datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")<datetime.datetime(2021,3,18)])
        self.df_season5=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime(2021,3,18)<=datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")<datetime.datetime(2021,4,23)])
        self.df_season6=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime(2021,4,23)<=datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")<datetime.datetime(2021,6,21)])
        self.df_season7=pd.DataFrame([df.loc[i] for i in range(len(df["teacher"])) if datetime.datetime(2021,6,21)<=datetime.datetime.strptime(df["date"][i],"%Y-%m-%d")])
        
        
    def season_pie(self,file_name=(str(datetime.datetime.today()))):
                
                
        ###１，０，NAの時期ごとの割合
        fig=plt.figure(dpi=300)
        
        pie_list_label=["0","1","NA"]
        
        ax1=fig.add_subplot(241)
        pie_list_value=(collections.Counter(self.df["teacher"].fillna("NA")))
        pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
        ax1.set_title("全体の比率")
        ax1.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)
        
        ax2=fig.add_subplot(242)
        pie_list_value=(collections.Counter(self.df_season1["teacher"].fillna("NA")))
        pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
        ax2.set_title("コロナ前")
        ax2.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)
        
        ax3=fig.add_subplot(243)
        pie_list_value=(collections.Counter(self.df_season2["teacher"].fillna("NA")))
        pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
        ax3.set_title("1回緊急事態宣言")
        ax3.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)
        
        ax4=fig.add_subplot(244)
        pie_list_value=(collections.Counter(self.df_season3["teacher"].fillna("NA")))
        pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
        ax4.set_title("GoTo")
        ax4.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)
        
        ax5=fig.add_subplot(245)
        pie_list_value=(collections.Counter(self.df_season4["teacher"].fillna("NA")))
        pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
        ax5.set_title("2回緊急事態宣言")
        ax5.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)
        
        ax6=fig.add_subplot(246)
        pie_list_value=(collections.Counter(self.df_season5["teacher"].fillna("NA")))
        pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
        ax6.set_title("蔓延防止法")
        ax6.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)
        
        ax7=fig.add_subplot(247)
        pie_list_value=(collections.Counter(self.df_season6["teacher"].fillna("NA")))
        pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
        ax7.set_title("3回緊急事態宣言")
        ax7.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)
        
        ax8=fig.add_subplot(248)
        pie_list_value=(collections.Counter(self.df_season7["teacher"].fillna("NA")))
        pie_list_value=[pie_list_value[0],pie_list_value[1],pie_list_value["NA"]]
        ax8.set_title("宣言解除後")
        ax8.pie(pie_list_value,labels=pie_list_label,startangle=90,counterclock=False)
        
        fig.show()
        file_name=file_name+".png"
        fig.savefig(file_name,bbox_inches='tight')
        
    def time_plot(self,file_name=(str(datetime.datetime.today()))):
        ###ツイート数の推移
        tweet_num_list=[len(self.df_season1),len(self.df_season2),len(self.df_season3),len(self.df_season4),len(self.df_season5),len(self.df_season6),len(self.df_season7)]
        fig=plt.figure(dpi=300)
        ax1=fig.add_subplot(111)
        ax1.plot(tweet_num_list)
        ax1.set_xticklabels(["","コロナ前","1回緊急事態宣言","GoToキャンペーン等","2回緊急事態宣言","蔓延防止法","3回緊急事態宣言","宣言解除後"],rotation=90)
        fig.show()
        file_name=file_name+".png"
        fig.savefig(file_name,bbox_inches='tight')