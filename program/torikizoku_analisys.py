import pandas as pd
import numpy as np
from janome.tokenizer import Tokenizer
from gensim.models.doc2vec import Doc2Vec
from sklearn.decomposition import PCA
from gensim.models.doc2vec import TaggedDocument
from sklearn.cluster import KMeans
import japanize_matplotlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from matplotlib import lines
import collections
import datetime

df=pd.read_csv("../data/torikizoku_twitter.csv")
import re
for i,tweet in enumerate(df["tweet"]):
    tmp1 = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', tweet)
    tmp2 = re.sub(r'(\d)([,.])(\d+)', r'\1\3', tmp1)
    df["tweet"][i] = re.sub(r'\d+', '0', tmp2)


class wakati:
    def __init__(self,df):
        self.df=df
        self.text_list=self.df["tweet"]
        self.t = Tokenizer()
        self.replace()
        self.main()
        self.merge()
        
    def replace(self):
        self.text_list_2=[]
        n=0
        for text in self.text_list:
            try:
                self.text_list_2.append(text.replace("\n",""))
                n+=1
            except:
                print("type=float",n)
                self.df.drop(n)
                n+=1

    def extract_words(self,text):
        tokens = self.t.tokenize(text)
        return [token.base_form for token in tokens 
            if token.part_of_speech.split(',')[0] in['名詞', '動詞']]
    
    def main(self):
        self.word_list = [self.extract_words(sentence) for sentence in self.text_list_2]
        
    def merge(self):
        self.df_2=pd.DataFrame({"date":self.df.date,
                                "ID":self.df.ID,
                                "tweet":self.word_list})
        self.df_2=self.df_2.reset_index(drop=True)



b=wakati(df)
word_list=b.word_list
df2=b.df_2

class doc_2_vbec:
    def __init__(self,df,size):
        self.df=df
        self.word_list=df["tweet"]
        self.vec_list=[]
        self.tag_list = [TaggedDocument(words=doc, tags=[i]) for i, doc in enumerate(self.word_list)]
        self.model=Doc2Vec(documents=self.tag_list,vector_size=size, window=5, min_count=5, workers=4)
        for i in range(len(self.word_list)):
            self.vec_list.append(list(self.model.dv.get_vector(i)))

        self.df_2=pd.DataFrame({"date":self.df["date"],
                                "ID":self.df["ID"],
                                "tweet":self.vec_list})

        
c=doc_2_vbec(df2,3)
main_df=c.df_2

class kmeans_twitter:
    def __init__(self,df):
        self.df=df
        self.word_list=df["tweet"]
        self.kmeans=KMeans(n_clusters=5)
        self.word_df=pd.DataFrame()
        for i in self.word_list:
            temp_df=pd.DataFrame(i)
            self.word_df=self.word_df.append(temp_df.T)
        self.word_array=np.array([self.word_df[0].tolist(),
                                  self.word_df[1].tolist(),
                                  self.word_df[2].tolist()],np.float64)
        self.word_array=self.word_array.T
        self.plot()
        
    def plot(self):
        self.fig = plt.figure(figsize = (8, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_title("鳥貴族ツイートのクラスタリング", size = 20)
        self.ax.set_xlabel("第1成分", size = 14)
        self.ax.set_ylabel("第2成分", size = 14)
        self.ax.set_zlabel("第3成分", size = 14)
        self.color=["red","blue","green","yellow","orange","purple","black","lightblue"]
        self.color_lsit=[]
        for i in list(self.kmeans.fit_predict(self.word_array)):
            self.color_lsit.append(self.color[i])
        self.ax.scatter(self.word_df[0],self.word_df[1],self.word_df[2],color=self.color_lsit)
        plt.show() 



d=kmeans_twitter(main_df)

c=doc_2_vbec(df2,100)
main_df=c.df_2


class kmeans_pca_twitter:
    def __init__(self,df_i):
        self.df=df_i
        self.word_list=self.df["tweet"]
        self.pca=PCA(n_components=3)
        self.kmeans=KMeans(n_clusters=3)
        self.word_df=pd.DataFrame()
        for i in self.word_list:
            temp_df=pd.DataFrame(i)
            self.word_df=self.word_df.append(temp_df.T)
        self.word_array=self.word_df.values
        self.pca.fit(self.word_array)
        self.for_kmeans=self.pca.fit_transform(self.word_array)
        self.fig = plt.figure(figsize = (8, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_title("鳥貴族ツイートのクラスタリング", size = 20)
        self.ax.set_xlabel("第1成分", size = 14)
        self.ax.set_ylabel("第2成分", size = 14)
        self.ax.set_zlabel("第3成分", size = 14)
        self.color=["red","blue","green","yellow","orange","purple","black","lightblue"]
        self.color_lsit=[]
        self.result_km=list(self.kmeans.fit_predict(self.for_kmeans))
        for i in self.result_km:
            self.color_lsit.append(self.color[i])
        self.dfdfdf=pd.DataFrame(self.for_kmeans)
        self.ax.scatter(self.dfdfdf[0],self.dfdfdf[1],self.dfdfdf[2],color=self.color_lsit)
        plt.show() 

e=kmeans_pca_twitter(main_df)
df["Unnamed: 0"]=e.result_km
df_1=pd.DataFrame()
df_2=pd.DataFrame()
df_3=pd.DataFrame()
df_4=pd.DataFrame()
df_5=pd.DataFrame()
df_1_param=pd.DataFrame()
df_2_param=pd.DataFrame()
df_3_param=pd.DataFrame()
df_4_param=pd.DataFrame()
df_5_param=pd.DataFrame()
for i,c in enumerate(e.result_km):
    if c ==0:
        df_1=df_1.append(df.iloc[i])
        df_1_param=df_1_param.append(e.dfdfdf.iloc[i])
    elif c==1:
        df_2=df_2.append(df.iloc[i])
        df_2_param=df_2_param.append(e.dfdfdf.iloc[i])
    elif c==2:
        df_3=df_3.append(df.iloc[i])
        df_3_param=df_3_param.append(e.dfdfdf.iloc[i])
    elif c==3:
        df_4=df_4.append(df.iloc[i])
        df_4_param=df_4_param.append(e.dfdfdf.iloc[i])
    elif c==4:
        df_5=df_5.append(df.iloc[i])
        df_5_param=df_5_param.append(e.dfdfdf.iloc[i])
pd.DataFrame(e.for_kmeans)

e.dfdfdf.describe()

df_1_param.describe()
df_2_param.describe()
df_3_param.describe()
df_4_param.describe()
df_5_param.describe()
pie_color=[]
for i in list(collections.Counter(e.result_km).keys()):
    pie_color.append(e.color[i])


df_season1=pd.DataFrame()
df_season2=pd.DataFrame()
df_season3=pd.DataFrame()
df_season4=pd.DataFrame()
df_season5=pd.DataFrame()
df_season6=pd.DataFrame()
df_season7=pd.DataFrame()



for i,date in enumerate(df["date"]):
    temp_date=datetime.datetime.strptime(date,"%Y-%m-%d")
    if temp_date<datetime.datetime(2020,4,7):
        df_season1=df_season1.append(df.iloc[i])
    elif temp_date<datetime.datetime(2020,5,25):
        df_season2=df_season2.append(df.iloc[i])
    elif temp_date<datetime.datetime(2021,1,7):
        df_season3=df_season3.append(df.iloc[i])
    elif temp_date<datetime.datetime(2021,3,18):
        df_season4=df_season4.append(df.iloc[i])
    elif temp_date<datetime.datetime(2021,4,23):
        df_season5=df_season5.append(df.iloc[i])
    elif temp_date<datetime.datetime(2021,6,21):
        df_season6=df_season6.append(df.iloc[i])
    else:
        df_season7=df_season7.append(df.iloc[i])

plt.pie(np.array(list(collections.Counter(e.result_km).values())),colors=pie_color)
plt.title("全体")
plt.show()
plt.pie(np.array(list(collections.Counter(df_season1["Unnamed: 0"]).values())),colors=pie_color)
plt.title("コロナ前")
plt.show()
plt.pie(np.array(list(collections.Counter(df_season2["Unnamed: 0"]).values())),colors=pie_color)
plt.title("1回緊急事態宣言")
plt.show()
plt.pie(np.array(list(collections.Counter(df_season3["Unnamed: 0"]).values())),colors=pie_color)
plt.title("GoToキャンペーン等")
plt.show()
plt.pie(np.array(list(collections.Counter(df_season4["Unnamed: 0"]).values())),colors=pie_color)
plt.title("2回緊急事態宣言")
plt.show()
plt.pie(np.array(list(collections.Counter(df_season5["Unnamed: 0"]).values())),colors=pie_color)
plt.title("蔓延防止法")
plt.show()
plt.pie(np.array(list(collections.Counter(df_season6["Unnamed: 0"]).values())),colors=pie_color)
plt.title("3回緊急事態宣言")
plt.show()
plt.pie(np.array(list(collections.Counter(df_season7["Unnamed: 0"]).values())),colors=pie_color)
plt.title("宣言解除後")
plt.show()

d_count=collections.Counter(df["date"])

lines.Line2D(d_count.keys(), d_count.values())

plt.plot(list(d_count.keys()), list(d_count.values()))

wakati_all_list=[]
for i in df2["tweet"]:
    wakati_all_list.extend(i)

all_count=collections.Counter(wakati_all_list)
all_count_sorted = sorted(all_count.items(), key=lambda x:x[1])
all_count.most_common(100)

df2_season1=pd.DataFrame()
df2_season2=pd.DataFrame()
df2_season3=pd.DataFrame()
df2_season4=pd.DataFrame()
df2_season5=pd.DataFrame()
df2_season6=pd.DataFrame()
df2_season7=pd.DataFrame()



for i,date in enumerate(df2["date"]):
    temp_date=datetime.datetime.strptime(date,"%Y-%m-%d")
    if temp_date<datetime.datetime(2020,4,7):
        df2_season1=df2_season1.append(df2.iloc[i])
    elif temp_date<datetime.datetime(2020,5,25):
        df2_season2=df2_season2.append(df2.iloc[i])
    elif temp_date<datetime.datetime(2021,1,7):
        df2_season3=df2_season3.append(df2.iloc[i])
    elif temp_date<datetime.datetime(2021,3,18):
        df2_season4=df2_season4.append(df2.iloc[i])
    elif temp_date<datetime.datetime(2021,4,23):
        df2_season5=df2_season5.append(df2.iloc[i])
    elif temp_date<datetime.datetime(2021,6,21):
        df2_season6=df2_season6.append(df2.iloc[i])
    else:
        df2_season7=df2_season7.append(df2.iloc[i])


class count_tweet_word:
    def __init__(self,df):
        wakati_all_list=[]
        for i in df["tweet"]:
            wakati_all_list.extend(i)
            self.all_count=collections.Counter(wakati_all_list)
        self.count_50=self.all_count.most_common(50)
        
season1_count=count_tweet_word(df2_season1)
season2_count=count_tweet_word(df2_season2)
season3_count=count_tweet_word(df2_season3)
season4_count=count_tweet_word(df2_season4)
season5_count=count_tweet_word(df2_season5)
season6_count=count_tweet_word(df2_season6)
season7_count=count_tweet_word(df2_season7)

freqe_word_list=[]

for i in all_count_sorted[-101:-1]:
    freqe_word_list.append(i[0])

season_1_freqe=[]
season_2_freqe=[]
season_3_freqe=[]
season_4_freqe=[]
season_5_freqe=[]
season_6_freqe=[]
season_7_freqe=[]



for i in freqe_word_list:
    season_1_freqe.append(season1_count.all_count[i]/sum(season1_count.all_count.values())*100)
    season_2_freqe.append(season2_count.all_count[i]/sum(season2_count.all_count.values())*100)
    season_3_freqe.append(season3_count.all_count[i]/sum(season3_count.all_count.values())*100)
    season_4_freqe.append(season4_count.all_count[i]/sum(season4_count.all_count.values())*100)
    season_5_freqe.append(season5_count.all_count[i]/sum(season5_count.all_count.values())*100)
    season_6_freqe.append(season6_count.all_count[i]/sum(season6_count.all_count.values())*100)
    season_7_freqe.append(season7_count.all_count[i]/sum(season7_count.all_count.values())*100)


for i in range(51):
    fig=plt.figure()
    fig.suptitle("「"+freqe_word_list[i]+"」の出現頻度")
    fig.add_subplot(111)
    ax1=plt.subplot(111)
    ax1.plot(np.array(["コロナ前","1回緊急事態宣言","GoToキャンペーン等","2回緊急事態宣言","蔓延防止法","3回緊急事態宣言","宣言解除後"]),np.array([season_1_freqe[i],season_2_freqe[i],season_3_freqe[i],season_4_freqe[i],season_5_freqe[i],season_6_freqe[i],season_7_freqe[i]]))
    plt.xticks(rotation=45)
    plt.show()


