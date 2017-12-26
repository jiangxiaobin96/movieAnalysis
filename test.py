import requests
import bs4
import pymysql

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
    for i in range(0, 50, 25):
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
            print(m_name + "        " + str(m_rating_score) + "           " + m_peoplecount + "    " + m_url)
            sql = "insert into movie(name,score,commentNum,link) values('"+m_name+"',"+str(m_rating_score)+",'"+m_peoplecount+"','"+m_url+"')"
            cursor.execute(sql)
            con.commit()

# except Exception as e:
#     con.rollback()
finally:
    con.close()