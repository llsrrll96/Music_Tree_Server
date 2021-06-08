import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os

from webdriver_manager.chrome import ChromeDriverManager

import db_connector

count = 0

# 발매일, 가사 검색을 위한 드라이버
def openDriver1(id):
    url = 'https://www.melon.com/song/detail.htm?songId=' + str(id)
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('headless')
    webdriver_options.add_argument('no-sandbox')
    # driver = webdriver.Chrome(options=webdriver_options)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(3)
    driver.get(url)
    time.sleep(1)
    return driver

# 발매일, 가사 검색
def searchMelon1(driver, data, index):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    dds = soup.find_all('dd')
    lyrics = soup.find(id='d_video_summary')

    day = dds[1].text
    try :
        lyric = lyrics.text.replace('\t', '').replace('\n', '').replace('"', '')
    except :
        lyric = ''

    data.iloc[index, 8] = day
    data.iloc[index, 9] = lyric
    # tempData = pd.DataFrame(data.iloc[index]).T
    # tempData.to_csv("melon6-2.csv", mode='a', index=False, encoding='utf-8-sig', header=False)
    # print(count)

    driver.quit()
    return data
    # return day

# 그룹, 젠더를 위한 드라이버
def openDriver2(id):
    url = 'https://www.melon.com/artist/detail.htm?artistId=' + str(id)
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('headless')
    webdriver_options.add_argument('no-sandbox')
    driver = webdriver.Chrome(options=webdriver_options)
    driver.implicitly_wait(3)
    driver.get(url)
    time.sleep(1)
    return driver

# 그룹, 젠더 검색
def searchMelon2(driver, data, k):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    dl = soup.find(class_='section_atistinfo03').find(class_='list_define clfix')
    groupGenderType = dl.find_all('dd')
    groupType = 3
    genderType = 0

    for i in groupGenderType:
        typeTemp = i.text
        if typeTemp.find('\t') != -1 :
            typeTemp = typeTemp.replace('\t', '').replace('\n', '').replace('"', '')
            typeList = typeTemp.split('|')
            if len(typeList) != 1:
                if typeList[1] == "남성":
                    genderType = 1
                elif typeList[1] == "여성":
                    genderType = 2
                elif typeList[1] == "혼성":
                    genderType = 3
                else :
                    genderType = 0
            else :
                genderType = 0

            if typeList[0] == "솔로":
                groupType = 1
            elif typeList[0] == "그룹":
                groupType = 2
            else :
                groupType = 3
            break

    data.iloc[k, 4] = groupType
    data.iloc[k, 5] = genderType
    tempData = pd.DataFrame(data.iloc[k]).T
    tempData.to_csv("finalMelonMusic.csv", mode='a', index=False, encoding='utf-8-sig', header=False)

    print(count)
    time.sleep(20)
    driver.quit()
    # return day

# 데이터를 DB에 넣기 전 한 번 더 중복값 체크
def songidSearch():
    # 중복값 체크를 위해 id값을 가져옴
    db = db_connector.DbConnector()
    db.connect()
    try:
        with db.connection.cursor() as cursor:
            sql = "SELECT melon_song_id FROM music_tree.song"
            cursor.execute(sql)
            result = cursor.fetchall()
            #result = pd.DataFrame(result, index = [0])
            list = []
            for i in result :
                list.append(i["melon_song_id"])
            #print(list)
            return list
    finally:
        db.close()

# 추가적인 크롤링(노래ID, 가사ID를 사용하여 추가적인 정보를 가져옴)을 진행 후 csv 완성
def fillCsv() :
    global count
    data = pd.read_csv("melonMusicList.csv", encoding='utf-8-sig', names=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    if not os.path.exists('finalMelonMusic.csv'):
        startIndex = 0
    else:
        startIndex = len(pd.read_csv("finalMelonMusic.csv", encoding='utf-8-sig', names=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]))
        count = startIndex

    for k in range(startIndex, len(data)) :
        count += 1
        driver = openDriver1(data.iloc[k, 0])
        data = searchMelon1(driver, data, k)
        driver = openDriver2(data.iloc[k, 1])
        searchMelon2(driver, data, k)

    data = pd.read_csv("finalMelonMusic.csv", encoding='utf-8-sig', names=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    data = data.drop(data.columns[1], axis=1)
    csvIdList = data.iloc[:, 0]
    dbIdList = songidSearch()
    print("-------------------------------")
    print("중복 제거 전 : " + str(len(data)))
    # print(len(data))

    for i in range(len(csvIdList) - 1, -1, -1):
        for j in range(len(dbIdList) - 1, -1, -1):
            if str(csvIdList[i]) == str(dbIdList[j]) :
                data = data.drop(data.index[i])
                break

    print("중복 제거 후 : " + str(len(data)))

    rs = insertDB(data)
    return rs

# DB에 노래 데이터 삽입
def insertDB(data) :
    db = db_connector.DbConnector()
    db.connect()

    try:
        for i in range(len(data)):
            list = data.iloc[i, :].tolist()
            with db.connection.cursor() as cursor:
                sql = "INSERT INTO music_tree.song (melon_song_id, title, artist, group_type, gender, " \
                      "album, genre, rel_date, lyrics, relevance, mood, feat) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, list)
                db.connection.commit()

        return 1
    except Exception as ex:  # 에러 종류
        return -1
        # print('에러가 발생 했습니다 \n', ex)  # ex는 발생한 에러의 이름을 받아오는 변수
    finally:
        db.close()

# fillCsv()