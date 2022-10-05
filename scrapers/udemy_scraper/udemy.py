
from bs4 import BeautifulSoup
import requests
import psycopg2
import time

# GetCoursesItems(): scrape free courses


def GetCoursesItems():
    html = requests.get(
        "https://coursevania.com/stm_lms_course_category/data-science/")
    soup = BeautifulSoup(html.content, 'lxml')
    courses = soup.find_all("div", class_="stm_lms_courses__single__inner")
    L = []
    for course in courses:
        link = course.a["href"]
        title = course.find(
            "div", class_="stm_lms_courses__single--title").a.h5.text
        details = Descr_link(link)
        L += [(title, details[0][1:-1], details[1])]
    lis = []
    for i in range(len(L)):
        lis += [L[len(L) - i - 1]]
    return lis

# Descr_link() : scrape description located in the detail page related to every course item


def Descr_link(item_link):
    html = requests.get(item_link)
    soup = BeautifulSoup(html.content, 'lxml')
    description = soup.find("div", class_="stm_lms_udemy_headline").text
    coupon_link = soup.find("div", class_="stm-lms-buy-buttons").a["href"]
    return (description, coupon_link)


# CheckNewArticles():  return new courses that may be added recently in order to insert it to the database
def CheckNewArticles():
    connection = psycopg2.connect(host="", database="datalands",
                                  user="postgres",
                                  port="5432",
                                  password="")
    cursor = connection.cursor()
    query = "select title from udemy limit 12;"
    cursor.execute(query)
    result = cursor.fetchall()
    previous_courses = []
    for a in result:
        previous_courses += [a[0]]
    cursor.close()
    connection.close()
    scraped = GetCoursesItems()

    articles_to_insert = []
    for item in scraped:
        if item[0] not in previous_courses:
            articles_to_insert += [item]
    return articles_to_insert

# InsertNEwArticles(): insert new articles to database


def InsertNewArticles():
    new_articles = CheckNewArticles()
    number_of_articles = len(new_articles)
    if number_of_articles == 0:
        return
    else:
        connection = psycopg2.connect(host="", database="datalands",
                                      user="postgres",
                                      port="5432",
                                      password="")
        cursor = connection.cursor()
        for i in range(number_of_articles):
            query = "insert into udemy(title, description, link) values (%s,%s,%s);"
            record = (new_articles[i][0], new_articles[i]
                      [1], new_articles[i][2])
            cursor.execute(query, record)
            connection.commit()
        cursor.close()
        connection.close()
        return


# _________main______
if __name__ == "__main__":
    InsertNewArticles()