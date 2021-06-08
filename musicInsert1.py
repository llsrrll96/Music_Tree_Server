from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller

import db_connector
import os

mList = []
count = 0

# 크롬드라이버 오토설치
def initialize() :
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인

    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')

    driver.implicitly_wait(10)

# 크롬드라이버를 통해 웹에 접근
def openDriver(startIndex, genre):
    #startIndex = 1
    url = 'https://www.melon.com/genre/song_list.htm?gnrCode=' + genre\
          + '#params%5BgnrCode%5D=' + genre\
          + '&params%5BdtlGnrCode%5D=GN0501&params%5BorderBy%5D=NEW&params%5BsteadyYn%5D=N&po=pageObj&startIndex='\
          + str(startIndex)
    # test = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0200#params%5BgnrCode%5D=GN0200&params%5BdtlGnrCode%5D=&params%5BorderBy%5D=POP&params%5BsteadyYn%5D=N&po=pageObj&startIndex=1"
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('headless')
    webdriver_options.add_argument('no-sandbox')
    # driver = webdriver.Chrome(options=webdriver_options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=webdriver_options)

    driver.implicitly_wait(3)
    driver.get(url)
    time.sleep(1)
    return driver

# 노래정보를 크롤링해오는 함수
def searchMelon(driver, grNumber):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all(class_='wrap_song_info')

    j = 0
    global count
    global mList
    maxCount = 1000

    for i in tags:
        try:
            songId_temp = i.find(class_='ellipsis rank01').a["href"]
            songId_start = songId_temp.find(",")
            songId_end = songId_temp.find(")")
            songId = songId_temp[songId_start + 1 : songId_end]
            singerId_temp = i.find(class_='ellipsis rank02').a["href"]
            singerId_start = singerId_temp.find("(")
            singerId_end = singerId_temp.find(")")
            singerId = singerId_temp[singerId_start + 2: singerId_end - 1]
            title = i.find(class_='ellipsis rank01').a.text
            singer = i.find(class_='ellipsis rank02').a.text
            album = tags[j + 1].find(class_='ellipsis rank03').a.text

            feat = ''
            featPoint = title.find('Feat.')
            if featPoint != -1 :
                featEnd = title.find(')')
                feat = title[featPoint + 6 : featEnd]
                feat = feat.replace(",","`")

            groupType = 0
            gender = 0
            if singer.find(',') != -1 :
                groupType = 3

            count += 1
            print(f'-----------------{count}-------------------')
            print(f'SONGID : {songId} \nSINGERID : {singerId} \n제목 : {title}\n가수 : {singer}\n'
                  f'그룹타입 : {groupType} \n성별 : {gender} \n앨범 : {album} \nfeat : {feat}')
            mList.append([songId, singerId, title, singer, groupType, gender, album, grNumber, '', '', '', 0, feat])
            j += 1
        except:
            j += 1
            pass
        if count == maxCount :
            break

    driver.quit()
    return mList

# 크롤링 결과값을 csv 형태로 서버 내에 저장
def saveToFile(filename, mList):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
    # with open(filename, 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(mList)

# 중복값 체크를 위해 id값을 가져옴
def songidSearch():
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

# 클라로부터 페이지 수와 장르값을 받아와 크롤링 하는 함수
def insertMusic(page, grNumber) :
    if os.path.exists('finalMelonMusic.csv'):
        os.remove('finalMelonMusic.csv')

    initialize()

    endPoint = 1 + (page * 50)
    genre = "GN0" + str(grNumber) + "00"
    for k in range(1, endPoint, 50) :
        driver = openDriver(k, genre)
        mList = searchMelon(driver, grNumber)

    csvIdList = []
    for l in mList :
        csvIdList.append(l[0])
    dbIdList = songidSearch()
    print("-------------------------------")
    print("중복 제거 전 : " + str(len(mList)))

    for i in range(len(csvIdList) - 1, -1, -1):
        for j in range(len(dbIdList) - 1, -1, -1):
            if str(csvIdList[i]) == str(dbIdList[j]) :
                # print(mList[i])
                mList.pop(i)
                break

    print("중복 제거 후 : " + str(len(mList)))
    saveToFile('melonMusicList.csv', mList)

    if os.path.exists('melonMusicList.csv'):
        return mList
    else :
        return -1

# insertMusic(1, 2)