# -*- coding: UTF-8 -*-
import requests
import bs4
import pymysql
import re
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba
import codecs
import os
from os import path
from scipy.misc import imread

con = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    db="movie",
    port=3306,
    use_unicode=True,
    charset="utf8"
)
cursor = con.cursor()
plt.figure(1)
plt.figure(2)
country = {}
property = {}


try:
    # 制片国家
    sql = "select country from movie"
    cursor.execute(sql)
    data = cursor.fetchall()
    con.commit()
    for i in range(len(data)):
        for j in range(len(data[i])):
            m_country = data[i][j].split(',')
            for x in m_country:
                if x in country.keys():
                    country[x] = country[x] + 1
                else:
                    country[x] = 1

    # 电影类型
    sql = "select property from movie"
    cursor.execute(sql)
    data = cursor.fetchall()
    con.commit()
    for i in range(len(data)):
        for j in range(len(data[i])):
            m_property = data[i][j].split(',')
            for x in m_property:
                if x in property.keys():
                    property[x] = property[x] + 1
                else:
                    property[x] = 1

    #国家的柱状图
    print(country.keys())
    print(country.values())
    print(country)
    x = country.keys()
    y = country.values()
    plt.figure(1)
    plt.xlabel("country")
    plt.ylabel("number")
    a = plt.subplot(1, 1, 1)
    plt.bar(x,y)
    plt.legend()



    #类型词云
    d = path.dirname(__file__)
    alice_coloring = imread(path.join(d,"2.png"))
    print("1")
    wc = WordCloud(
        background_color="white",
        mask=alice_coloring,
        font_path='C:\Windows\Fonts\STZHONGS.TTF',
        stopwords=STOPWORDS,
        max_font_size=40,
        random_state=42
    )
    print(property)
    wc.generate_from_frequencies(property)
    image_colors = ImageColorGenerator(alice_coloring)

    # 以下代码显示图片
    plt.figure(2)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()





# except Exception as e:
#     con.rollback()
finally:
    con.close()