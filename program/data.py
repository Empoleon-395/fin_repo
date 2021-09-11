import pandas as pd
from janome.tokenizer import Tokenizer

df=pd.read_csv("../data/umbrella_rev.csv")
txt_title=list(df["rev_title"])
txt_content=list(df["rev_text"])
text=Tokenizer()

err_index_title=[]
title_list=[]
n=0
for i in txt_title:
    try:   
        temp_list=text.tokenize(i)
        temp_list_1=[]
        for token in temp_list:
            temp_list_1.append(str(token.base_form))
        title_list.append(temp_list_1)
        n+=1
    except:
        err_index_title.append(n)
        print("エラー",n)
        

err_index_content=[]
content_list=[]
n=0
for i in txt_content:
    try:
        temp_list=text.tokenize(i)
        temp_list_1=[]
        for token in temp_list:
            temp_list_1.append(str(token.base_form))
        content_list.append(temp_list_1)
        n+=1
    except:
        err_index_content.append(n)
        print("エラー",n)

for i in err_index_content:
    title_list.pop(i)
for i in err_index_title:
    content_list.pop(i)
    
err_index_title.extend(err_index_content)
err_index=list(set(err_index_title))
df_1=df.drop(err_index)

df_2=pd.DataFrame({"star":(df_1["rev_star"]),
                   "text":content_list})
df_3=df_2.reset_index()
for_uni_text=[]
for i in range(len(df_3["text"])):
    for j in df_3["text"][i]:
        if len(j)==0 or len(j)==1 or "n" in j or j=="です" or j=="ます" or j=="ある" or j=="思う" or j=="する" or j=="ので" or j=="いる":
            df_3["text"][i].remove(j)
    for_uni_text.extend(df_3["text"][i])
uni_text=set(for_uni_text)
text_count={}
for i in uni_text:
    text_count[i]=for_uni_text.count(i)
    
    
df_4=pd.DataFrame()
for j in range(len(df_3)):
    text_count={}
    text_count["star"]=[int(bool(df_3["star"][j]>3))]
    for i in uni_text:
        text_count[i]=(df_3["text"][j].count(i))
    df_4=df_4.append(text_count,ignore_index=True)
    print(j)
