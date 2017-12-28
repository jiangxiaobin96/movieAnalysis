import requests
import bs4
import pymysql
import re
import matplotlib.pyplot as plt
import matplotlib

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
country = {}
property = {}
plt.xlabel("country")
plt.ylabel("number")
a = plt.subplot(1,1,1)
zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\consola.ttf')

try:
    for i in range(0, 25, 25):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(str(i))
        # print(url)
        req = requests.get(url)
        req.encoding="utf-8"
        #print(req.text)
        contents = req.text
        soup = bs4.BeautifulSoup(contents,"html.parser")
        print("豆瓣电影TOP250" + "\n" +" 影片名              评分       评价人数     链接 ")
        for tag in soup.find_all('div',class_='info'):
            m_name = tag.find('span',class_='title').get_text()
            m_rating_score = float(tag.find('span', class_='rating_num').get_text())
            m_people = tag.find('div', class_="star")
            m_span = m_people.findAll('span')
            m_peoplecount = m_span[3].contents[0]
            m_url = tag.find('a').get('href')

            req = requests.get(m_url)
            req.encoding = "utf-8"
            # print(req.text)
            contents = req.text
            soup = bs4.BeautifulSoup(contents, "html.parser")
            for tag2 in soup.find_all('div', id='info'):
                # print(str(tag2))
                m_countrylist = re.findall("<span class=\"pl\">制片国家/地区:</span>(.*)<br/>",str(tag2))
                countrylist = m_countrylist[0].split('/')
                for i in countrylist:
                    j = i.strip()
                    print(country.keys())
                    if j in country.keys():
                        country[j] = country[j] + 1
                    else:
                        country[j] = 1
                # m_propertylist = re.findall("<span property=\"v:genre\">(.*?)</span>",str(tag2))
                # print(m_propertylist)
                # for i in m_propertylist:
                #     if i in property:
                #         property[i] += 1
                #     else:
                #         property[i] = 1
    print(country.keys())
    print(country.values())
    print(country)
    x = country.keys()
    y = country.values()
    plt.bar(x,y)
    plt.legend(prop=zhfont1)
    plt.show()

                # m_country = ','.join(m_countrylist)
                # m_property = ','.join(m_propertylist)
                # print(m_country)
                # print(m_property)

            # print(m_name + "        " + str(m_rating_score) + "           " + m_peoplecount + "    " + m_url)
#             sql = "insert into movie(name,score,commentNum,link,country,property) values('"+m_name+"',"+str(m_rating_score)+",'"+m_peoplecount+"','"+m_url+"','"+m_country+"','"+m_property+"')"
#             cursor.execute(sql)
#             con.commit()
#
#
# except Exception as e:
#     con.rollback()
finally:
    con.close()