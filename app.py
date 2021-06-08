# -*- coding: utf-8 -*-

import json

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit, join_room, leave_room

import Administrator
import musicInsert1
import musicInsert2
import question
import result_manager
import pandas as pd
import datetime
import numpy as np
import math
from db_connector import DbConnector
import lyrics_find
import copy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.debug = True
app.host = 'localhost'

cors = CORS(app, resources={
    r"/song-info": {"origin": "*"},
    r"/admin/delete": {"origin": "*"},
    r"/admin/add1": {"origin": "*"},
    r"/admin/add2": {"origin": "*"},
    r"/admin/modify": {"origin": "*"}
})
socketIo = SocketIO(app, cors_allowed_origins="*")


## 관리자 #####################################################

@app.route("/")
def main():
    return render_template("index.html")


# 노래 업데이트 1단계 : 노래 정보를 크롤링을 통해 따온 후 관리자에게 목록을 제공한다.
@app.route('/admin/add1', methods=["GET"])
def songAdd1():
    pg = request.args.get('page')
    gr = request.args.get('grNumber')

    if pg is None or gr is None:
        data = {
            "result": "args error"
        }
        return data

    # print(str(test) + str(gr))
    rs = musicInsert1.insertMusic(int(pg), int(gr))

    if rs != int(-1):
        list = []
        for i in range(len(rs)):
            # resultArray.append([])
            dict = {"title": rs[i][2], "artist": rs[i][3]}
            list.append(dict)
        jsonArray = json.dumps(list, ensure_ascii=False)
        print(jsonArray)

        return jsonArray
    else:
        data = {
            "result": "none count"
        }
        return data


# 목록을 확인한 관리자가 추가를 승인할 경우, 해당 목록들의 곡들이 DB에 업데이트 된다.
@app.route('/admin/add2', methods=["GET"])
def songAdd2():
    rs = musicInsert2.fillCsv()

    if rs != int(-1):
        data = {
            "result": "yes"
        }
        return data
    else:
        data = {
            "result": "error"
        }
        return data


# 목록을 확인한 관리자가 추가를 승인할 경우, 해당 목록들의 곡들이 DB에 업데이트 된다.
# @app.route('/filterList', methods=["GET"])
def filterList(data):
    socket_id = data["socketId"]
    step = session[socket_id]['step']
    btnValue = data["btnValue"]
    print(step)
    print(btnValue)
    sub_list = session[socket_id]['song_list']
    print(sub_list)
    col = -1
    value = ""

    if step == 1:
        col = '8'
        if btnValue == "남성":
            value = 1
        elif btnValue == "여성":
            value = 2
        elif btnValue == "혼성":
            value = 3
        elif btnValue == "기타":
            value = 0
        idx = sub_list[sub_list[col] != int(value)].index
    elif step == 2:
        col = '7'
        if btnValue == "솔로":
            value = 1
        elif btnValue == "그룹":
            value = 2
        elif btnValue == "기타":
            value = 3
        idx = sub_list[sub_list[col] != int(value)].index
    elif step == 3:
        col = '6'
        if btnValue == "발라드":
            value = 1
        elif btnValue == "댄스":
            value = 2
        elif btnValue == "랩/힙합":
            value = 3
        elif btnValue == "R&B/Soul":
            value = 4
        elif btnValue == "인디음악":
            value = 5
        elif btnValue == "록/메탈":
            value = 6
        elif btnValue == "트로트":
            value = 7
        elif btnValue == "포크/블루스":
            value = 8
        idx = sub_list[sub_list[col] != int(value)].index
    elif step == 4:
        col = '5'
        value = str(btnValue)[0:3]
    elif step == 5:
        col = '4'
    elif step == 6:
        col = '9'
    elif step == 7:
        col = '11'
        if btnValue == "자극적인":
            value = 1
        elif btnValue == "화난":
            value = 2
        elif btnValue == "긴장되는":
            value = 3
        elif btnValue == "슬픈":
            value = 4
        elif btnValue == "지루한":
            value = 5
        elif btnValue == "졸린":
            value = 6
        elif btnValue == "잔잔한":
            value = 7
        elif btnValue == "평화로운":
            value = 8
        elif btnValue == "느긋한":
            value = 9
        elif btnValue == "기쁜":
            value = 10
        elif btnValue == "행복한":
            value = 11
        elif btnValue == "신나는":
            value = 12
        idx = sub_list[sub_list[col] != int(value)].index
    elif step == 8:
        col = '10'
        value = btnValue
        idx = sub_list[sub_list[col] != str(value)].index

    print(col)
    print(value)

    if step == 4:
        idx = sub_list[sub_list[col] != int(value)].index
    elif step == 5 or step == 6:
        if btnValue == "예":
            idx = sub_list[sub_list[col] == ""].index
        elif btnValue == "아니요":
            idx = sub_list[sub_list[col] != ""].index
    # else :
    #    idx = sub_list[sub_list[col] != str(value)].index
    print(idx)

    sub_list = sub_list.drop(idx)
    session[socket_id]['song_list'] = sub_list
    print(sub_list)
    session[socket_id]['step'] = step + 1


# 접속하는 url
@app.route('/song-info', methods=['GET'])
def song():
    # db 조회
    index = request.args.get('index')  # /song-info?index=
    result = Administrator.song_inquiry(int(index))
    for i in result:
        i['id'] = i['song_id']
        del i['song_id']

    print(result)
    return jsonify(result)


# 관리자 노래 수정
@app.route('/admin/modify', methods=['POST'])
def admin_modify():
    input = request.get_json()
    # input = {
    #                 "id" : 1,
    #                 "relevance" : "관련성",
    #                 "mood" : "분위기",
    #                 "lyrics" : "가사",
    #                 "words" : ""
    #         }
    data = [input['relevance'], input['mood'], input['lyrics'], input['words'], input['id']]
    status = Administrator.song_modify(data)  # 수행 결과. 수정된 row 갯수 반환.
    if status == 1:
        status = "yes"
    else:
        status = "no"
    return jsonify({"result": status})


# 관리자 노래 삭제
@app.route('/admin/delete', methods=['POST'])
def admin_delete():
    input = request.get
    id = input.form.get('id')
    status = Administrator.song_delete(id)
    if status == 1:
        status = "yes"
    else:
        status = "no"
    return jsonify({"result": status})


# 관리자 가사 단어 추출
@app.route('/admin/words', methods=['POST'])
def admin_update_words():
    Administrator.update_words_all()

    return jsonify({"result": 1})


# 소켓 #####################################################
# socket_id : 유저를 구분하는 id
# session[socket_id]의 형태로 바로 접근하도록 dictionary로 설정
# session[socket_id]['song_list'] : 노래 정보 배열 저장

@socketIo.on('disconnect', namespace='/prediction')
def disconnect():
    # socket_id = data["socketId"]
    # leave_room(socket_id)
    # session[socket_id].clear()
    print("Disconnected")


@socketIo.on('join', namespace='/prediction')
def on_join(data):
    print("join enter")
    socket_id = data["socketId"]
    global song_list

    join_room(socket_id)
    session[socket_id] = {}
    # session[socket_id]['song_list'] = copy.deepcopy(song_list)

    sub_list = pd.DataFrame(song_list)
    sub_list.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
    sub_list['5'] = pd.to_datetime(sub_list['5'])
    sub_list['5'] = sub_list['5'].dt.year
    for i in sub_list.index:
        sub_list['5'][i] = str(sub_list['5'][i])[0:3]
        if sub_list['4'][i] != 1.0:
            sub_list['4'][i] = ""
        if sub_list['9'][i] == "\r" or sub_list['9'][i] is None:
            sub_list['9'][i] = ""

    # print(song_list)
    print(sub_list['4'])
    print(sub_list['9'])
    session[socket_id]['song_list'] = copy.deepcopy(sub_list)
    session[socket_id]['step'] = 1
    print("test2")

    data = {
        "result": "yes"
    }
    emit('join_response', data, to=socket_id)


@socketIo.on('answer', namespace='/prediction')
def answerRequest(ans):
    print("ans: ", ans)
    socket_id = ans["socketId"]
    # 데이터 보내는 함수 생성
    # 프로토콜 type 1: 일반질문, 2: 가사 ,3: 결과
    data = {
        "type": "1",
        "result": ans
    }

    filterList(ans)

    # data = {
    #             "type" : "1",
    #             "step": "2",
    #             "q":"2번 질문입니다.",
    #             'socketId': session['socketId']
    #         }
    # data = {
    #             "type" : "2"
    #         }
    # data = {
    #             "type" : "3",
    #             "songId" : Result.getSongId()
    #         }

    # print(data)
    # 보내는 데이터
    emit('answer', data, to=socket_id)

    return None


# 가사 검색
@socketIo.on('lyrics_find', namespace='/prediction')
def find_lyrics(data):
    socket_id = data["socketId"]
    lyrics_input = data["lyricsInput"]
    sub_list = lyrics_find.df_to_dict(session[socket_id]['song_list'].to_dict('records'))
    session[socket_id]['song_list'] = sub_list
    song_answer_arr = []
    cnt = 0

    if lyrics_input == '':
        for i in range(len(sub_list)):
            song_answer_arr.append(sub_list[i])
            cnt += 1
    else:
        lf = lyrics_find.LyricsFind(lyrics_input, sub_list)
        song_id = lf.max_similarity()
        for i in range(len(sub_list)):
            if song_id == sub_list[i]['song_id']:
                song_answer_arr.append(sub_list[i])
                break

    for i in range(len(song_answer_arr)):
        song_answer_arr[i]['url'] = result_manager.search_song_url(song_answer_arr[i]['artist'], song_answer_arr[i]['title'])
        song_answer_arr[i]['rel_date'] = str(song_answer_arr[i]['rel_date'])

    # answer['song_answer_arr'][0]['lyrics']의 형태로 접근
    answer = {'type': '3', 'song_answer_arr': song_answer_arr}
    emit('answer', answer, to=socket_id)


# 질문 생성
@socketIo.on('question', namespace='/prediction')
def make_question(data):
    socket_id = data["socketId"]
    step = session[socket_id]['step']

    question_type = [[
        "남성", "여성", "혼성", "기타"  # 성별.
    ], [
        "솔로", "그룹", "기타"  # 활동유형.
    ], [
        "발라드", "댄스", "랩/힙합", "R&B/Soul", "인디음악", "록/메탈", "트로트", "포크/블루스"  # 장르.
    ], [
        2020, 2010, 2000, 1990, 1980  # 년도.
    ], [
        "예", "아니요"  # OST 여부.
    ], [
        "예", "아니요"  # 피처링 여부.
    ], [
        "자극적인", "화난", "긴장되는", "슬픈", "지루한", "졸린", "잔잔한", "평화로운", "느긋한", "기쁜", "행복한", "신나는"  # 분위기.
    ], [  # 관련성.
    ]]
    question_type_name = ["성별", "활동유형", "장르", "년도", " OST여부", "피처링여부", "분위기", "관련성"]

    isNone = False  # song_list가 비어있는지 여부
    if step == 8:
        sub_list = session[socket_id]['song_list']
        if len(sub_list) == 0:
            # song_list가 빈 경우 관련성 질문 X, 다음 step ( 가사 검색 ) 으로 넘어감
            step += 1
            isNone = True
        else:
            relevance = []
            for i in sub_list.index:
                relevance.append(sub_list['10'][i])
                if len(relevance) == 10:
                    break
            question_type[7] = relevance

    if step == 9:
        if isNone:
            # song_list가 빈 경우 실패 메세지도 같이 전송
            data = {
                "type": "2",
                "result": "failure"
            }
        else:
            data = {
                "type": "2"
            }
    else:
        data = {
            "type": "1",
            "step": step,  # 1: 성별, 2: 활동유형, 3:장르, 4:년도, 5:OST 여부, 6:피처링 여부, 7:분위기, 8:관련성
            "question_type_name": question_type_name[step - 1],  # 질문에 나올 질문할 속성 명
            "question_type": question_type[step - 1],  # 답변으로 표시될 노래 속성값들
        }

    emit('response', data, to=socket_id)


# https://flask-socketio.readthedocs.io/en/latest/
if __name__ == "__main__":
    db = DbConnector()
    song_list = db.select_all()
    for i in range(len(song_list)):
        song_list[i]['words'] = song_list[i]['words'].split()
    print(len(song_list))
    socketIo.run(app, host='0.0.0.0', port=5000)

# app.run(debug=True)
# host 등을 직접 지정하고 싶다면
# app.run(host="127.0.0.1", port="5000", debug=True)
