import pymysql
import bs4
import requests
import re


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

try:
    for i in range(0, 25, 25):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(str(i))
        # print(url)
        req = requests.get(url)
        req.encoding="utf-8"
        #print(req.text)
        contents = req.text
        soup = bs4.BeautifulSoup(contents,"html.parser")
        # print("豆瓣电影TOP250" + "\n" +" 影片名              评分       评价人数     链接 ")
        for tag in soup.find_all('div',class_='info'):
            m_name = tag.find('span',class_='title').get_text()
            m_rating_score = float(tag.find('span', class_='rating_num').get_text())
            m_people = tag.find('div', class_="star")
            m_span = m_people.findAll('span')
            m_peoplecount = m_span[3].contents[0]
            m_url = tag.find('a').get('href')

            if m_url == "https://movie.douban.com/subject/5912992/":
                continue
            req = requests.get(m_url)
            req.encoding = "utf-8"
            # print(req.text)
            contents = req.text
            soup = bs4.BeautifulSoup(contents, "html.parser")
            for tag2 in soup.find_all('div', id='info'):

                m_countrylist = re.findall("<span class=\"pl\">制片国家/地区:</span>(.*)<br/>",str(tag2))
                m_propertylist = re.findall("<span property=\"v:genre\">(.*?)</span>",str(tag2))

                countrylist = m_countrylist[0].split('/')
                m_country = ""
                for i in countrylist:
                    j = i.strip()
                    m_country = m_country + "," + j
                m_country = m_country.strip(",")
                m_property = ','.join(m_propertylist)

            for tag3 in soup.find_all('div', class_='rating_wrap clearbox'):
                stars = re.findall("<span class=\"rating_per\">(.*)</span>",str(tag3))
                five = stars[0]
                four = stars[1]
                three = stars[2]
                two = stars[3]
                one = stars[4]

            print(m_name + "        " + str(m_rating_score) + "           " + m_peoplecount + "    " + m_url)
            sql = "insert into movie(name,score,commentNum,link,country,property,five_star,four_star,three_star,two_star,one_star) values('"+m_name+"',"+str(m_rating_score)+",'"+m_peoplecount+"','"+m_url+"','"+m_country+"','"+m_property+"','"+five+"','"+four+"','"+three+"','"+two+"','"+one+"')"
            cursor.execute(sql)
            con.commit()

            comment_url = m_url + "/comments?status=P"
            req = requests.get(comment_url)
            req.encoding = "utf-8"
            # print(req.text)
            contents = req.text
            movieName = re.findall("<title>(.*) 短评</title>", str(contents))
            # print(movieName)
            username = re.findall("<a href=\"https://www.douban.com/people/(.*)/\" class=\"\">", str(contents))
            stars = re.findall("<span class=\"allstar(.*) rating", str(contents))

            sql = "select Id from movie where name=" + "'" + movieName[0] + "'"
            # print(sql)
            cursor.execute(sql)
            data = cursor.fetchone()
            con.commit()

            movieId = str(data[0])
            for i in range(len(stars)):
                sql = "insert into commentDetail(movieId,stars,username) values(" + "'" + movieId + "'," + "'" + stars[i] + "'," + "'" + username[i] + "')"
                print(sql)
                cursor.execute(sql)
                con.commit()

# except Exception as e:
#     con.rollback()
finally:
    con.close()