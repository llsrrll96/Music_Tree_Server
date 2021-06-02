# Music_Tree_Server

## Rest API Server

### Data Protocol
```

- input
  - join 
    data = {socketId : socket.id}
   
  - answer
        data = {
            "btnValue" : "버튼 값",
            "socketId" : "소켓 id 문자열"
        }

- output
        data = {
               "type": "1",
               "step": step,  # 1: 성별, 2: 활동유형, 3:장르, 4:년도, 5:OST 여부, 6:피처링 여부, 7:분위기, 8:관련성
               "question_type_name": question_type_name[step-1],  #질문에 나올 질문할 속성 명 ex) "성별"
               "question_type": question_type[step-1]  #답변으로 표시될 노래 속성값들 ,  ex) ["남성","여성"]
       }
```
            
#### 가사 검색 요청
```
- output
    data = {
                "type" : "2"
            }
```

#### 노래 예측 결과결과
```
- input 
    data = {socketId : socket.id, lyricsInput : lyrics}
    가사 모름 :
    data = {socketId : socket.id, lyricsInput : ''}

- output
    data = {
        'song_id': 2, 
        'title': "롤린 (Rollin')", 
        'artist': '브레이브걸스', 
        'album': "Rollin'", 
        'ost': None, 
        'rel_date': datetime.date(2017, 3, 7), 
        'genre': 2, 
        'group_type': 2, 
        'gender': 2,
         'feat': '\r', 
         'relevance': '사랑', 
         'mood': 11, 
         'lyrics': "그 날을 잊지 못해 babe 날 보며 환히 웃던 너의 미소에 홀린 듯 I'm fall in love But 너무 쪽팔림에 난 그저 한마디 말도 못해 babe I wanna you 너의 눈빛은 날 자꾸 네 곁을 맴돌게 해 Just only you 굳게 닫힌 내 맘이 어느새 무너져버려 Because of you 온통 너의 생각뿐이야 나도 미치겠어 너무 보고 싶어 매일 매일 매일 자꾸 초라해지잖아 내 모습이 그대여 내게 말해줘 사랑한다고 Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' 하루가 멀다 하고 Rolling in the deep Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' 기다리고 있잖아 Babe Just only you 기다리고 있잖아 Babe Just only you Hey I just wanna be with you 오늘 밤이 가기 전에 I can't feel you 조금 더 다가와 줘 Tonight I'm ready for you You wanna touch me I know 대체 뭘 고민해 빨리 안아 아닌 척 모르는 척 하다가 늦게 놓치고 후회 말아 I wanna you 너의 눈빛은 날 자꾸 네 곁을 맴돌게 해 Just only you 굳게 닫힌 내 맘이 어느새 무너져버려 Because of you 온통 너의 생각뿐이야 나도 미치겠어 너무 보고 싶어 매일 매일 매일 자꾸 초라해지잖아 내 모습이 그대여 내게 말해줘 사랑한다고 Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' 하루가 멀다 하고 Rolling in the deep Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' 기다리고 있잖아 Babe Just only you 이제 와 숨기려 하지 마요 그대여 아닌 척하지 마요 온종일 난 그대 생각에 잠긴 채로 난 이대로 기다리고 있어요 Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' 하루가 멀다 하고 Rolling in the deep Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' Rollin' 기다리고 있잖아 Babe Just only you 기다리고 있잖아 Babe Just only you", 
         'words': None, 
         'melon_song_id': 30287019, 
         'type': '3', 
         'url': 'https://www.youtube.com/watch?v=-Axm4IYHVYk'
         }
```

#### 노래 조회
```
- input 
     /song-info?index=1
     index = 1 ,51 ,101 ,,,
- output
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
        }
    ]
```

#### 노래 수정
```
- input
    input = {
                "id" : 1,
                "relevance" : "관련성",
                "mood" : "분위기",
                "lyrics" : "가사",
                "words" : ""
            }
    
- output
    data = { "result" : "yes" } 
```

#### 노래 삭제
```
- input 
    POST, <class 'list'> 배열 형태
    input = [4, 5]
    
- output
    data = { "result" : "yes" }
```

#### 노래 추가
```
- input
    add2
- output
    data = { "result" : "yes" } 
            { "result" : "no" }
```
```
- input
    add1?page=1&grNumber, GET
    page = 1 ~ 10 , grNumber = 1 ~ 8 
- output
[
        {
                title: "사랑 안 해",
                artist: "백지영"
        },
        {
                title: "불꽃놀이",
                artist: "하진"
        }
]
```
