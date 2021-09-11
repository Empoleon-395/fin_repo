import pandas as pd
from janome.tokenizer import Tokenizer

df=pd.read_csv("../data/umbrella_rev.csv")
df=df.drop(3246).reset_index(drop=True)
txt_title=list(df["rev_title"])
txt_content=list(df["rev_text"])
txt_content_list=[]
n=0
for i in txt_content:
    try:
        txt_content_list.append(i.replace("\n",""))
        n+=1
    except:
        print("float",i,n)
        n+=1


# Tokenizerインスタンスの生成 
t = Tokenizer()

# テキストを引数として、形態素解析の結果、名詞・動詞・形容詞(原形)のみを配列で抽出する関数を定義 
def extract_words(text):
    tokens = t.tokenize(text)
    return [token.base_form for token in tokens 
        if token.part_of_speech.split(',')[0] in['名詞', '動詞']]

#  関数テスト
# ret = extract_words('三四郎は京都でちょっと用があって降りたついでに。')
# for word in ret:
#    print(word)

# 全体のテキストを句点('。')で区切った配列にする。 
# それぞれの文章を単語リストに変換(処理に数分かかります)
n=0
err_index_content=[]
for i in txt_content:
    try:
        word_list = [extract_words(sentence) for sentence in txt_content]
        n+=1
        print(n)
    except:
        err_index_content.append(n)
        n+=1
        print("エラー",n)
df["rev_text"][0].replace("\n","")

import pickle
f = open('../data/word_list.txt', 'wb')
pickle.dump(word_list,f)
f = open("../data/word_list.txt","rb")
list_row = pickle.load(f)
