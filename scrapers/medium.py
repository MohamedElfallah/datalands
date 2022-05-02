from bs4 import BeautifulSoup
import time
from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import psycopg2


def GetArticles():
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    op.add_argument("--disable-dev-shm-usage")
    op.add_argument("--no-sandbox")
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=op)

    url = "https://medium.com/topic/data-science"

    driver.get(url)
    time.sleep(3)

    # scrolling down the page
    for i in range(2):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(3)

    # Scraping Data
    soup = BeautifulSoup(driver.page_source, 'lxml')
    sections = soup.find_all("div", class_="l ep ki")
    list = []
    for section in sections:
        try:
            link = section.find(
                "a")['href']
            title = section.find(
                "h2", class_="bn fw ko kp kq kr ga ks kt ku kv ge kw kx ky kz gi la lb lc ld gm le lf lg lh gq gr gs gt gv gw fu").text
            description = section.find(
                "p", class_='li b do dp gr lz gs gt ma gv gw iq fu').text
        except:
            continue
        if "https://" not in link:
            link = "https://medium.com"+link
        list += [(title, description, link)]
    revers = []
    for i in range(len(list)):
        revers += [list[len(list)-i-1]]
    return revers


def CheckNewArticles():
    scraped = GetArticles()
    print(len(scraped))
    connection = psycopg2.connect(host="192.168.75.3", database="datalands",
                                  user="postgres",
                                  port="5432",
                                  password="mytestdb")
    cursor = connection.cursor()
    query = "select title from medium limit 85;"
    cursor.execute(query)
    result = cursor.fetchall()
    previous_courses = []
    for a in result:
        previous_courses += [a[0]]
    cursor.close()
    connection.close()
    articles_to_insert = []
    for item in scraped:
        if item[0] not in previous_courses:
            articles_to_insert += [item]
    print(len(articles_to_insert))
    return articles_to_insert


def insert():
    new_articles = CheckNewArticles()
    number_of_articles = len(new_articles)
    if number_of_articles == 0:
        return
    else:
        connection = psycopg2.connect(host="192.168.75.3", database="datalands",
                                      user="postgres",
                                      port="5432",
                                      password="mytestdb")
        cursor = connection.cursor()
        for i in range(number_of_articles):
            query = "insert into medium(title, description, link) values (%s,%s,%s);"
            record = (new_articles[i][0], new_articles[i]
                      [1], new_articles[i][2])
            cursor.execute(query, record)
            connection.commit()
        cursor.close()
        connection.close()
        return


if __name__ == "__main__":
    i=1
    while(True):
        insert()
        print("processed medium :", i)
        i+=1
        time.sleep(30)
