import pandas as pd
import datetime
from selenium import webdriver
driver=webdriver.Chrome()
driver.get("https://www.amazon.co.jp/%E3%83%AC%E3%83%87%E3%82%A3%E3%83%BC%E3%82%B9-%E6%8A%98%E3%82%8A%E3%81%9F%E3%81%9F%E3%81%BF%E5%82%98-UV%E3%82%AB%E3%83%83%E3%83%88%E7%8E%87100-%E9%9B%A8%E3%81%AB%E6%BF%A1%E3%82%8C%E3%82%8B%E3%81%A8%E6%A1%9C%E6%9F%84%E3%81%8C%E6%B5%AE%E3%81%8D%E5%87%BA%E3%82%8B%E5%82%98-%E5%8F%8E%E7%B4%8D%E3%83%9D%E3%83%BC%E3%83%81%E4%BB%98%E3%81%8D/product-reviews/B07RGZJM5T/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")
all_reviews=driver.find_element_by_css_selector('a[data-hook="see-all-reviews-link-foot"]')
all_reviews.click()

star_element=driver.find_elements_by_css_selector('i[data-hook="review-star-rating"]')
star=[]
for i in star_element:
    star.append(int(i.get_attribute("class")[26]))

title_element=driver.find_elements_by_css_selector('[data-hook="review-title"]')
title=[]
for i in title_element:
    title.append(i.text)
   
date_element=driver.find_elements_by_css_selector('span[data-hook="review-date"]')
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

next_p=driver.find_element_by_css_selector('li[class="a-last"]')
next_p.click()        
