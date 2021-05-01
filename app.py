# -*- coding: utf-8 -*-

import os
import question, result
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, send, emit, join_room,leave_room
from lyrics_find import LyricsFind
from db_connector import DbConnector


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.debug = True
app.host = 'localhost'

socketIo = SocketIO(app, cors_allowed_origins="*")

user_no = 1

@socketIo.on('start', namespace='/prediction')
def connect(v):
    print('start')
    global user_no
    if 'session' in session and 'user-id' in session:
        pass
    else:
        session['session'] = os.urandom(24)
        session['username'] = 'user' + str(user_no)
        user_no += 1
    # emit("response", {'data': 'Connected', 'username': session['username']})

    emit("response", question.firstQuestion(session['username']), broadcast=False)

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
                "type" : "3",
                "songId" : Result.getSongId()
            }
    print(data)
    # data = {
    #             "type" : "1",
    #             "step": "2",
    #             "q":"2번 질문입니다.",
    #             'username': session['username']
    #         }

    # data = {
    #             "type" : "3",
    #             "songId" : Result.getSongId()
    #         }

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
