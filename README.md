# Music_Tree_Server

## Rest API Server

### Data Protocol
    data = {
                "type" : "1",
                "step": "2",
                "q":"2번 질문입니다.",
                'socketId': session['socketId']
            }
            
#### 가사 검색 요청  
    data = {
                "type" : "2"
            }
#### 결과
    data = {
                "type" : "3",
                "songId" : Result.getSongInfo()
            }
#### 노래 정보
    song = {
        "title" : title,
        "artist" : artist,
        "album" : album,
        "genre" : genre,
        "lyric" : lyric
    }
