# Music_Tree_Server

## Rest API Server

### Data Protocol
```
- output
        data = {
               "type": "1",
               "step": step,  # 1: 성별, 2: 활동유형, 3:장르, 4:년도, 5:OST 여부, 6:피처링 여부, 7:분위기, 8:관련성
               "question_type_name": question_type_name[step-1],  #질문에 나올 질문할 속성 명, ["남성","여성"]
               "question_type": question_type[step-1]  #답변으로 표시될 노래 속성값들 , "성별"
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
    data = { 
                "title" : "제목".
                "artist" : "가수"
            }
```
