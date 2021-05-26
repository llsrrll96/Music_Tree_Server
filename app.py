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
from db_connector import DbConnector
from lyrics_find import LyricsFind

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.debug = True
app.host = 'localhost'

cors = CORS(app, resources={
    r"/song-info": {"origin": "*"},
    r"/admin/delete": {"origin": "*"},
    r"/admin/add1": {"origin": "*"},
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
    """
    data = {
        "result": "yes"
    }
    return data
    """


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


# 접속하는 url
@app.route('/song-info', methods=['GET'])
def song():
    # db 조회
    index = request.args.get('index')  # /song-info?index=
    result = Administrator.song_inquiry(int(index))
    for i in result:
        i['id'] = i['song_id']
        del i['song_id']

    # test 더미데이터
    data = [
        {
            "id": 1,
            "title": "song_title",
            "artist": "song_artist",
            "album": "song_album",
            "ost": 2,
            "rel_date": "2020-12-12",
            "genre": 3,
            "group_type": 4,
            "gender": 5,
            "feat": "피쳐링",
            "relevance": "관련성",
            "mood": "분위기",
            "lyrics": "가사",
            "words": "",
        },
        {
            "id": 2,
            "title": "song_title",
            "artist": "song_artist",
            "album": "song_album",
            "ost": 2,
            "rel_date": "2020-12-12",
            "genre": 3,
            "group_type": 4,
            "gender": 5,
            "feat": "피쳐링",
            "relevance": "관련성",
            "mood": "분위기",
            "lyrics": "가사",
            "words": ""
        },
        {
            "id": 3,
            "title": "song_title",
            "artist": "song_artist",
            "album": "song_album",
            "ost": 2,
            "rel_date": "2020-12-12",
            "genre": 3,
            "group_type": 4,
            "gender": 5,
            "feat": "피쳐링",
            "relevance": "관련성",
            "mood": "분위기",
            "lyrics": "가사",
            "words": ""
        },
        {
            "id": 4,
            "title": "song_title",
            "artist": "song_artist",
            "album": "song_album",
            "ost": 2,
            "rel_date": "2020-12-12",
            "genre": 3,
            "group_type": 4,
            "gender": 5,
            "feat": "피쳐링",
            "relevance": "관련성",
            "mood": "분위기",
            "lyrics": "가사",
            "words": ""
        },
        {
            "id": 5,
            "title": "song_title",
            "artist": "song_artist",
            "album": "song_album",
            "ost": 2,
            "rel_date": "2020-12-12",
            "genre": 3,
            "group_type": 4,
            "gender": 5,
            "feat": "피쳐링",
            "relevance": "관련성",
            "mood": "분위기",
            "lyrics": "가사",
            "words": ""
        },
        {
            "id": 6,
            "title": "song_title",
            "artist": "song_artist",
            "album": "song_album",
            "ost": 2,
            "rel_date": "2020-12-12",
            "genre": 3,
            "group_type": 4,
            "gender": 5,
            "feat": "피쳐링",
            "relevance": "관련성",
            "mood": "분위기",
            "lyrics": "가사ㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇ",
            "words": ""
        }
    ]
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


## 소켓 #####################################################

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
    socket_id = data["socketId"]
    join_room(socket_id)
    session[socket_id] = {}
    session[socket_id]['song_list'] = song_list
    session[socket_id]['step'] = 1

    emit("response", question.create_question(socket_id), to=socket_id)


@socketIo.on('answer', namespace='/prediction')
def answerRequest(ans):
    print("ans: ", ans)
    socket_id = ans["socketId"]
    # 데이터 보내는 함수 생성
    # 프로토콜 type 1: 일반질문, 2: 가사 ,3: 결과
    data = {
        "type": "2"
    }
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

    print(data)
    # 보내는 데이터

    return None


# 가사 검색
@socketIo.on('lyrics_find', namespace='/prediction')
def find_lyrics(data):
    socket_id = data["socketId"]
    lyrics_input = data["lyricsInput"]
    lf = LyricsFind(lyrics_input, session[socket_id]['song_list'])
    song_id = lf.max_similarity()
    song_answer = session[socket_id]['song_list'][song_id]
    url = result_manager.search_song_url(song['artist'], song['title'])
    answer = {
        "type": "3",
        "song": song_answer,
        "url": url,
    }

    send('answer', answer, to=socket_id)


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

    if step == 8:
        song_list = session[socket_id]['song_list']
        question_type[7] = song_list['relevance']

    data = {
        "type": "1",
        "step": step,  # 1: 성별, 2: 활동유형, 3:장르, 4:년도, 5:OST 여부, 6:피처링 여부, 7:분위기, 8:관련성
        "question_type_name": question_type_name[step - 1],  # 질문에 나올 질문할 속성 명
        "question_type": question_type[step - 1],  # 답변으로 표시될 노래 속성값들
    }
    session[socket_id]['step'] = step + 1

    emit('response', data, to=socket_id)


# https://flask-socketio.readthedocs.io/en/latest/
if __name__ == "__main__":
    db = DbConnector()
    song_list = db.select_all()
    print(len(song_list))
    socketIo.run(app)

# app.run(debug=True)
# host 등을 직접 지정하고 싶다면
# app.run(host="127.0.0.1", port="5000", debug=True)
