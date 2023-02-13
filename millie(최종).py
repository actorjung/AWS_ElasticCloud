id = input("아이디를 입력하세요 : ")
pw = input("비밀번호를 입력하세요 : ")


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
import time
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import xlwt

driver = webdriver.Chrome("C:/Users/김근영/chromedriver_win32.zip/chromedriver.exe")

# 칼럼 리스트 준비
book_list = []

# 밀리의 서재 베스트셀러 웹페이지를 가져옵니다.(여기까지 로그인)
driver.get("https://www.millie.co.kr/v3/login")
time.sleep(0.5)
driver.find_element(By.CSS_SELECTOR, '#input-14').send_keys(id)
time.sleep(0.5)
driver.find_element(By.CSS_SELECTOR, '#input-15').send_keys(pw)
driver.find_element(By.CSS_SELECTOR, "#wrap > section > div > div.login-content > div.button-area.mt16 > button").click()
time.sleep(3)

#주간 웹페이지 들어가는 중
driver.find_element(By.CSS_SELECTOR, "#wrap > div > div > header > nav > ul > li:nth-child(3) > a").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#wrap > section > section > div.search-body > section.shortcuts > div > a.best-link.gtm-search-direct-best").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#wrap > section > div > section > article:nth-child(1) > h2").click()
time.sleep(1)

soup = BeautifulSoup(driver.page_source, 'html.parser')



# 1위 책 클릭(대여 횟수 긁어오기 위함)
for i in range(1, 101):#1위부터 100위까지
    driver.find_element(By.CSS_SELECTOR, "#wrap > section > div > section > article > ul > li:nth-child("+str(i)+") > div").click()
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    books = soup.select('div.cover-data')

    for book in books:
        title = book.select('p.book-name')[0].text
        author = book.select('p.author')[0].text
        borrow_num = book.select('strong')[0].text
        print(i, title, author, borrow_num)
        book_list.append([i, title, author, borrow_num])
    i += 1
    driver.find_element(By.CSS_SELECTOR, "#wrap > div > div > header > nav > ul > li:nth-child(3) > a").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#wrap > section > section > div.search-body > section.shortcuts > div > a.best-link.gtm-search-direct-best").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#wrap > section > div > section > article:nth-child(1) > h2").click()
    time.sleep(1)
    

    
df = pd.DataFrame(book_list, columns = ["순위", "제목", "저자", "대여 횟수"])


df.to_csv("밀리의 서재 대여 횟수" + '.csv', index = False, encoding = 'utf-8-sig')
df.to_excel("밀리의 서재 대여 횟수" + '.xls', index = False, encoding = "utf-8-sig")