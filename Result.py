def getSongInfo():
    #db 를 통해서 정보를 가져온다.
    title= 'title'
    artist= 'artist'
    album = 'album'
    genre = 'genre'
    lyric = 'lyric'

    song = {
        "title" : title,
        "artist" : artist,
        "album" : album,
        "genre" : genre,
        "lyric" : lyric
    }
    return song

def getSongId():
    return '12345'