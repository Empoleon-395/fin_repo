import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
import datetime
from selenium import webdriver
import re

class amazon_review:
    def __init__(self,words):
        self.driver=webdriver.Chrome()
        self.words=words
        self.search()
        self.item_select(3)
        self.item_url=list(dict.fromkeys(self.item_url))
        self.df=pd.DataFrame()
        for i in self.item_url:
            try:
                self.driver.get(i)
                time.sleep(2)
                self.get_iteminfo()
                while True:
                    temp_df=self.get_reviews()
                    self.df=pd.concat([self.df,temp_df])
                    try:
                        next_p=self.driver.find_element_by_css_selector('li[class="a-last"]')
                        next_p.click()
                        time.sleep(2)
                    except:
                        break
            except:
                print("レビューなし")
        
    def search(self):
        self.driver.get("https://www.amazon.co.jp/")
        time.sleep(1)
        box=self.driver.find_element_by_id("twotabsearchtextbox")
        box.send_keys(self.words)
        box.send_keys(Keys.ENTER)
        self.url=self.driver.current_url
        
    def item_select(self,num):
        self.items=self.driver.find_elements_by_css_selector('[class="a-link-normal a-text-normal"]')
        self.item_url=[]
        for i in self.items:
            self.item_url.append(i.get_attribute("href"))
            
    def get_iteminfo(self):
        name_element=self.driver.find_element_by_id("productTitle")
        self.name=name_element.text
        price_element=self.driver.find_element_by_id('price_inside_buybox')
        self.price=re.sub(r"\D", "",price_element.text)
        all_reviews=self.driver.find_element_by_css_selector('[data-hook="see-all-reviews-link-foot"]')
        all_reviews.click()
        time.sleep(2)

    def get_reviews(self):
        star_element=self.driver.find_elements_by_css_selector('i[data-hook="review-star-rating"]')
        star=[]
        for i in star_element:
            star.append(i.get_attribute("class")[26])
        
        title_element=self.driver.find_elements_by_css_selector('a[data-hook="review-title"]')
        title=[]
        for i in title_element:
            title.append(i.text)
           
        date_element=self.driver.find_elements_by_css_selector('span[data-hook="review-date"]')
        date=[]
        for i in date_element:
            y=i.text.find("年")
            year=int(i.text[0:y])
            m=i.text.find("月")
            month=int(i.text[y+1:m])
            d=i.text.find("日")
            day=int(i.text[m+1:d])
            temp_date=datetime.date(year,month,day)
            date.append(temp_date)
        
        text_element=self.driver.find_elements_by_css_selector('span[data-hook="review-body"]')
        text=[]
        for i in text_element:
            text.append(i.text)

        ret_df=pd.DataFrame({"item_name":self.name,
                         "price":self.price,
                         "rev_date":date,
                         "rev_star":star,
                         "rev_title":title,
                         "rev_text":text
                         })
        return ret_df

a=amazon_review("傘")
u=a.df.drop_duplicates(keep="first")
u.to_csv("../data/umbrella_rev.csv")
