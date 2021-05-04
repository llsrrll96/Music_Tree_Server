# Music_Tree_Server

## Rest API Server

### Data Protocol
```
- output
    data = {
                "type" : "1",
                "step": "2",
                "q":"2번 질문입니다.",
                'socketId': session['socketId']
            }
```
            
#### 가사 검색 요청
```
- output
    data = {
                "type" : "2"
            }
```

#### 결과
```
- output
    data = {
                "type" : "3",
                "songId" : Result.getSongInfo()
            }
```

#### 노래 결과 정보 (예측 끝)
```
- output
    song = {
        "title" : title,
        "artist" : artist,
        "album" : album,
        "genre" : genre,
        "lyric" : lyric
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
    input = {"1" : {"lyrics" : {"value" : "가사"}}}
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
    add?page=1&grNumber, GET
    page = 1 ~ 10 , grNumber = 1 ~ 8 
- output
    data = { "result" : "yes" } 
            { "result" : "no" }
```
