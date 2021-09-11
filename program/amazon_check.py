from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver=webdriver.Chrome()
driver.get("https://www.amazon.co.jp/ref=nav_logo")
login=driver.find_element_by_class_name("a-button-text")
login.click()
mail_box=driver.find_element_by_id("ap_email")
mail_box.send_keys("taka.yu9000@gmail.com")
mail_box.send_keys(Keys.ENTER)
pass_box=driver.find_element_by_id("ap_password")
pass_box.send_keys("y1u2i3op")
pass_box.send_keys(Keys.ENTER)
driver.get("https://www.amazon.co.jp/%E3%83%9D%E3%82%B1%E3%83%A2%E3%83%B3%E3%82%AB%E3%83%BC%E3%83%89%E3%82%B2%E3%83%BC%E3%83%A0-%E3%82%BD%E3%83%BC%E3%83%89-%E3%82%B7%E3%83%BC%E3%83%AB%E3%83%89-%E5%BC%B7%E5%8C%96%E6%8B%A1%E5%BC%B5%E3%83%91%E3%83%83%E3%82%AF-%E3%82%A4%E3%83%BC%E3%83%96%E3%82%A4%E3%83%92%E3%83%BC%E3%83%AD%E3%83%BC%E3%82%BA/dp/B08WB9FZ5D")
