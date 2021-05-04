# -*- coding: utf-8 -*-

import os
import question, result
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit, join_room,leave_room
from flask_cors import CORS
from db_connector import DbConnector
import Administrator
from lyrics_find import LyricsFind
import musicInsert1
import musicInsert2
import json
from collections import OrderedDict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.debug = True
app.host = 'localhost'

cors = CORS(app, resources={
    r"/song-info" : {"origin": "*"},
    r"/admin/delete": {"origin": "*"},
    r"/admin/add1": {"origin": "*"},
    r"/admin/modify": {"origin":"*"}
})
socketIo = SocketIO(app, cors_allowed_origins="*")

## 관리자 #####################################################

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/admin/add1', methods=["GET"])
def songAdd():
    pg = request.args.get('page')
    gr = request.args.get('grNumber')
    # print(str(test) + str(gr))
    rs = musicInsert1.insertMusic(int(pg), int(gr))

    if rs != int(-1) :
        list = []
        for i in range(len(rs)) :
            # resultArray.append([])
            dict = { "title" : rs[i][2], "artist" : rs[i][3]}
            list.append(dict)
        jsonArray = json.dumps(list, ensure_ascii=False)
        print(jsonArray)

        return jsonArray
    else :
        data = {
            "result": "error"
        }
        return data
    """
    data = {
        "result": "yes"
    }
    return data
    """

# 접속하는 url
@app.route('/song-info', methods=['GET'])
def song():
    # db 조회
    index = request.args.get('index')  # /song-info?index=
    result = Administrator.song_inquiry(int(index))
    # test 더미데이터
    data = [
        {
            "id" : 1,
            "title" : "song_title",
            "artist" : "song_artist",
            "album" : "song_album",
            "ost" : 2,
            "rel_date" : "2020-12-12",
            "genre" : 3,
            "group_type" : 4,
            "gender" : 5,
            "feat" : "피쳐링",
            "relevance" : "관련성",
            "mood" : "분위기",
            "lyrics" : "가사",
            "words" : "",
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


#관리자 노래 수정
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


#관리자 노래 삭제
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

session = {}

@socketIo.on('disconnect', namespace='/prediction')
def disconnect(data):
	socket_id = data["socketId"]
	leave_room(socket_id)
	del session[socket_id]
	print ("Disconnected")


@socketIo.on('join', namespace='/prediction')
def on_join(data):
	socket_id = data["socketId"]
	join_room(socket_id)
	session['socket_id'] = {}
# emit("response", question.firstQuestion(session['socket_id']), to=socketId)
	send('response', { "socketId" : socket_id }, to=socket_id)


	
@socketIo.on('answer',namespace='/prediction')
def requestl(ans):
	print("ans: ",ans)
	socket_id = ans["socketId"]
	# 데이터 보내는 함수 생성
	# 프로토콜 type 1: 일반질문, 2: 가사 ,3: 결과
	data = {
                "type" : "2"
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
	#보내는 데이터
	send("answer", data, to=socket_id)
	data.clear()

	return None


@socketIo.on('lyrics_find', namespace='/prediction')
def find_lyrics(data):

	socket_id = data["socketId"]
	lyrics_input = data["lyricsInput"]
	song_list = session[socket_id]['song_list']
	lf = LyricsFind(lyrics_input, song_list)
	song_id = lf.max_similarity()
	result = {
		"type" : "3",
		"song_id" : song_id
	}

	send('answer', result, to=socket_id)

# @app.route('/',methods=('GET', 'POST')) # 접속하는 url
# def index():
#     if request.method == "POST":
#         # user=request.form['user'] # 전달받은 name이 user인 데이터
#         print(request.form.get('user')) # 안전하게 가져오려면 get
#         user = request.form.get('user')
#         data = {'level': 60, 'point': 360, 'exp': 45000}
#         return render_template('index.html', user=user, data=data)
#     elif request.method == "GET":
#         user = "반원"
#         data = {'level': 60, 'point': 360, 'exp': 45000}
#         return render_template('index.html', user=user, data=data)


#https://flask-socketio.readthedocs.io/en/latest/
if __name__=="__main__":
	socketIo.run(app)

  # app.run(debug=True)
  # host 등을 직접 지정하고 싶다면
  # app.run(host="127.0.0.1", port="5000", debug=True)
