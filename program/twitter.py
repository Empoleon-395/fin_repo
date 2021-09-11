from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
from datetime import date
from datetime import datetime
from datetime import timedelta

class twitter_scrape:
    def __init__(self,word):
        self.word=word
        self.driver=webdriver.Chrome()
        self.err_date=[]
        self.main_df=pd.DataFrame()
        self.driver.get("https://twitter.com/search?q=%E9%B3%A5%E8%B2%B4%E6%97%8F%20since%3A2020-4-7_0%3A0%3A0_JST%20until%3A2020-4-7-23_23%3A59%3A59_JST&src=typed_query&f=live")
        time.sleep(2)
        self.daterange()
        self.main()


    def scrape(self,date,words="ポケモン"):
        self.box=self.driver.find_element_by_css_selector('input[placeholder="キーワード検索"]')
        self.box.send_keys(Keys.CONTROL + "a")
        self.box.send_keys(Keys.DELETE)
        self.box.send_keys(words)
        self.box.send_keys(Keys.ENTER)
        temp_list=[]
        self.temp_part_df=pd.DataFrame()
        self.tweet_text=[]
        self.tweet_text_list=[]
        while True:
            time.sleep(2)
            self.n=0
            self.tweet_content_list=self.driver.find_elements_by_css_selector('article[role="article"]')
            if len(self.tweet_content_list)==0:
                self.err_check(date)
            for i in self.tweet_content_list:
                try:
                    tt=i.find_element_by_css_selector('div[lang="ja"]')
                    self.tweet_text_list.append(tt.text)    
                    self.tweet_text.append(i.text)
                except:
                    print("not_japanese")
            if self.tweet_content_list==temp_list:
                break
            else:
                temp_list=self.tweet_content_list
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1200);")

        self.ID_list=[]
        for i in self.tweet_text:
            ii=i.replace(' ', '')
            iii=ii.replace('　', '')
            self.ID_list.append(iii.split()[1])
        temp_df=pd.DataFrame({"ID":self.ID_list,
                              "tweet":self.tweet_text_list})
        temp_df=temp_df.drop_duplicates(keep="first")
        self.temp_part_df=self.temp_part_df.append(temp_df)

    def scrape2(self,date,words="ぽけもん"):
        self.box=self.driver.find_element_by_css_selector('input[placeholder="キーワード検索"]')
        self.box.send_keys(Keys.CONTROL + "a")
        self.box.send_keys(Keys.DELETE)
        self.box.send_keys(words)
        self.box.send_keys(Keys.ENTER)
        temp_list=[]
        self.temp_part_df=pd.DataFrame()
        self.tweet_text=[]
        self.tweet_text_list=[]
        while True:
            time.sleep(2)
            self.n=0
            self.tweet_content_list=self.driver.find_elements_by_css_selector('article[role="article"]')
            if len(self.tweet_content_list)==0:
                self.err_check2()
            for i in self.tweet_content_list:
                try:
                    tt=i.find_element_by_css_selector('div[lang="ja"]')
                    self.tweet_text_list.append(tt.text)    
                    self.tweet_text.append(i.text)
                except:
                    print("not_japanese")
            if self.tweet_content_list==temp_list:
                break
            else:
                temp_list=self.tweet_content_list
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1200);")

        self.ID_list=[]
        for i in self.tweet_text:
            ii=i.replace(' ', '')
            iii=ii.replace('　', '')
            self.ID_list.append(iii.split()[1])
        temp_df=pd.DataFrame({"ID":self.ID_list,
                              "tweet":self.tweet_text_list})
        temp_df=temp_df.drop_duplicates(keep="first")
        self.temp_part_df=self.temp_part_df.append(temp_df)
        
    def search(self,words="ポケモン"):
        self.box=self.driver.find_element_by_css_selector('input[placeholder="キーワード検索"]')
        self.box.send_keys(Keys.CONTROL + "a")
        self.box.send_keys(Keys.DELETE)
        self.box.send_keys(words)
        self.box.send_keys(Keys.ENTER)

    def daterange(self,_start=datetime.strptime('2020-01-01', '%Y-%m-%d'), _end=datetime.strptime(str(date.today()), '%Y-%m-%d')):
        self.date=[]
        for n in range((_end - _start).days):
            self.date.append(str((_start + timedelta(n)).date()))

    def create_word(self,date):
        self.serch_word=self.word+" since:"+str(date)+"_0:0:0_JST until:"+str(date)+"_23:59:59"
        
    def return_df(self,date):
        temp_df=pd.DataFrame({"date":date,
                              "ID":self.temp_part_df["ID"],
                              "tweet":self.temp_part_df["tweet"]})
        self.main_df=self.main_df.append(temp_df)

    def err_check(self,date):
        self.err_date.append(date)
        self.n=1

    def err_check2(self):
        self.n=1

    def main(self):
        nn=0
        for date in self.date:
            if nn<10:
                self.driver.delete_all_cookies()
                self.create_word(date)
                self.scrape(date,self.serch_word)
                self.return_df(date)
                nn+=1
            else:
                nn=0
                self.driver.close()
                self.driver=webdriver.Chrome()
                self.driver.get("https://twitter.com/search?q=%E9%B3%A5%E8%B2%B4%E6%97%8F%20since%3A2020-4-7_0%3A0%3A0_JST%20until%3A2020-4-7-23_23%3A59%3A59_JST&src=typed_query&f=live")
                time.sleep(2)
                self.create_word(date)
                self.scrape(date,self.serch_word)
                self.return_df(date)
        while True:
            if len(self.err_date)!=0:
                self.driver.delete_all_cookies()
                nn=0
                for date in self.err_date:
                    if nn<10:
                        self.create_word(date)
                        self.scrape2(date,self.serch_word)
                        if self.n==0:
                            self.err_date.remove(date)
                        self.return_df(date)
                        nn+=1
                    else:
                        self.driver.close()
                        self.driver=webdriver.Chrome()
                        self.driver.get("https://twitter.com/search?q=%E9%B3%A5%E8%B2%B4%E6%97%8F%20since%3A2020-4-7_0%3A0%3A0_JST%20until%3A2020-4-7-23_23%3A59%3A59_JST&src=typed_query&f=live")
                        time.sleep(2)
                        self.create_word(date)
                        self.scrape2(date,self.serch_word)
                        if self.n==0:
                            self.err_date.remove(date)
                        self.return_df(date)
                        nn=0
            else:
                break




import os
os.chdir("C:/Users/takah/Dropbox/My PC (DESKTOP-4MU76QI)/Desktop/卒論用/program")
a=twitter_scrape("ディズニーランド")
df=a.main_df
df.to_csv("../data/disny_twitter.csv")


