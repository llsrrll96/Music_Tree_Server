# -*- coding: utf-8 -*-

import os
import question, result
from flask import Flask, render_template, request, session, jsonify
from flask_socketio import SocketIO, send, emit, join_room,leave_room
from flask_cors import CORS
from db_connector import DbConnector
from Music_Tree_Server import Administrator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.debug = True
app.host = 'localhost'

cors = CORS(app, resources={
    r"/song-info" : {"origin": "*"}
})
socketIo = SocketIO(app, cors_allowed_origins="*")

## 관리자 #####################################################

@app.route("/")
def main():
    return render_template("index.html")

# 접속하는 url
@app.route('/song-info', methods=['GET'])
def song():
    # db 조회
    index = request.args.get('index')  # /song-info?index=
    result = Administrator.song_inquiry(index)
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
    # input = {"id" : {"type_name" : {"value" : "?"}}}
    id = list(input)[0]
    type_name = list(input.get(id))[0]
    value = list(input.get(id).get(type_name))[0]
    status = Administrator.song_modify([type_name, value, id])  # 수행 결과. 수정된 row 갯수 반환.
    if status == 1:
        status = "yes"
    else:
        status = "no"
    return jsonify({"result": status})


#관리자 노래 삭제
@app.route('/admin/delete', methods=['POST'])
def admin_delete():
    input = request.get_json()
    id = input.get("id")
    status = Administrator.song_delete(int(id))
    if status == 1:
        status = "yes"
    else:
        status = "no"
    return jsonify({"result": status})

## 소켓 #####################################################

@socketIo.on('disconnect', namespace='/prediction')
def disconnect():
    session.clear()
    print ("Disconnected")

@socketIo.on('join', namespace='/prediction')
def on_join(data):
    socketId = data['socketId']
    join_room(socketId)
    session['socketId'] = socketId
    emit("response", question.firstQuestion(session['socketId']), to=socketId)

@socketIo.on("answer",namespace='/prediction')
def requestl(ans):
    print("ans: ",ans)
    # 데이터 보내는 함수 생성
    ## 프로토콜 type 1: 일반질문, 2: 가사 ,3: 결과
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

    print(data) #보내는 데이터
    emit("answer", data, broadcast=False)
    data.clear()

    return None

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

#####세션 관리#####
# user_no = 1
# @app.before_request
# def before_request():
#     global user_no
#     if 'session' in session and 'user-id' in session:
#         pass
#     else:
#         session['session'] = os.urandom(24) #랜덤값 부여
#         session['username'] = 'user'+str(user_no)
#         user_no += 1

#https://flask-socketio.readthedocs.io/en/latest/
if __name__=="__main__":
	socketIo.run(app)

  # app.run(debug=True)
  # host 등을 직접 지정하고 싶다면
  # app.run(host="127.0.0.1", port="5000", debug=True)
