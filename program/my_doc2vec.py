# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 16:48:01 2021

@author: takah
"""
import pandas as pd
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument


class my_doc2vec:
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
        
    def return_df(self):
        return self.df_2
    
    def similar_words(self,word,num=10):
        ret = self.model.wv.most_similar(positive=[word],topn=num) 
        for item in ret:
            print(item[0], item[1])
    
    def similar_2words(self,word1,word2,num=10):
        ret = self.model.wv.most_similar(positive=[word1,word2],topn=num) 
        for item in ret:
            print(item[0], item[1])