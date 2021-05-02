# -*- coding: utf-8 -*-

import os
import question, result
from flask import Flask, render_template, request, session, jsonify
from flask_socketio import SocketIO, send, emit, join_room,leave_room
from db_connector import DbConnector


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.debug = True
app.host = 'localhost'

socketIo = SocketIO(app, cors_allowed_origins="*")

## 관리자 #####################################################

@app.route("/")
def main():
    return render_template("index.html")

# 접속하는 url
@app.route('/song-info')
def song():
    # db 조회

    # test 더미데이터
    data = [
        {
            "song_id" : 1,
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
            "words" : ""
         },
        {
            "song_id": 2,
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
        }
    ]
    print(data)
    return jsonify(data)

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
def request(ans):
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
