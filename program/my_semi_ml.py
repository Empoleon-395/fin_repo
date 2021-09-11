# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 16:48:01 2021

@author: takah
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


class my_semi_ml:
    def fit(self,df,initial_t):
        self.df=df
        self.teacher_list=[np.nan]*len(self.df)
        self.teacher_list[0:len(initial_t)]=initial_t
        
        y_data=[i for i in self.teacher_list if np.isnan(i)==False]
        x_data=[self.df["tweet"][i] for i in range(len(self.teacher_list)) if np.isnan(self.teacher_list[i])==False]
        x_df=pd.DataFrame(x_data)
        x_y_df=pd.merge(x_df,pd.DataFrame({"teacher":y_data}),left_index=True,right_index=True)
        pd.DataFrame({"teacher":y_data})
        while True:
            n=0
            
            y_data=[i for i in self.teacher_list if np.isnan(i)==False]
            x_data=[self.df["tweet"][i] for i in range(len(self.teacher_list)) if np.isnan(self.teacher_list[i])==False]
            x_df=pd.DataFrame(x_data)
            x_y_df=pd.merge(x_df,pd.DataFrame({"teacher":y_data}),left_index=True,right_index=True)
            pd.DataFrame({"teacher":y_data})
            
            if len(x_y_df)<1000:
                self.bm,self.bs,bp=self.croval_rf(x_y_df)
            else:
                self.bm,self.bs,self.bp=self.hold_rf(x_y_df)
            
            new_teacher=self.bm.predict_proba(pd.DataFrame(list(self.df["tweet"])))
        
            if sum(np.isnan(self.teacher_list))==0:
                print("全てに教師データがついたため停止しました。")
                break
            
            for i in range(len(self.teacher_list)):
                if np.isnan(self.teacher_list[i]):
                    if new_teacher[:,1][i]>=0.85:
                        self.teacher_list[i]=1
                        print("add 1 in ",i)
                        n=1
                    elif new_teacher[:,1][i]<=0.1:
                        self.teacher_list[i]=0
                        n=1
            
            if n==0:
                print("教師データがこれ以上増えないため停止します。")
                break
            else:
                nn=sum(np.isnan(self.teacher_list))
                print("残り : ",nn)

    def croval_rf(self,df):
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
    
    def hold_rf(self,df):
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
    
    def return_df(self,df):
        rt_df=df.merge(pd.DataFrame({"teacher":self.teacher_list}),left_index=True,right_index=True)
        rt_df_good=rt_df[rt_df["teacher"]==1]
        rt_df_bad=rt_df[rt_df["teacher"]==0]
        return rt_df ,rt_df_good,rt_df_bad

    
    