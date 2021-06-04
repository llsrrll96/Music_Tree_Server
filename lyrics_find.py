from numpy import dot
from numpy.linalg import norm
import numpy as np
from konlpy.tag import Kkma, Okt, Hannanum
import time
from db_connector import DbConnector


# ex)
# lyrics_input : '니 손 꼭 잡고 그냥 이 길을 걸었으면 내게'
# lyrics_list : [{'song_id':1, 'words':['a', 'b', 'c'], 'lyrics':'asdjklfasdkfj'}, {'song_id':2, 'words':['b', 'c', 'd'], 'lyrics':'zcvmzncv,msdlf'}, ...]

class LyricsFind:
    def __init__(self, lyrics_input, lyrics_list):
        self.lyrics_input = lyrics_input
        self.lyrics_list = lyrics_list

    def compare_lyrics(self, lyrics):
        for l in self.lyrics_list:
            if l['lyrics'].find(lyrics) != -1:
                print(l['song_id'], l['title'], '노래와 매칭됨')
                return l['song_id']

        return 0

    def cosine_similarity(self, a, b):
        return dot(a, b) / (norm(a) * norm(b))

    # 노래 가사와 입력된 가사의 코사인 유사도 측정 후 유사도 반환
    def measure_similarity(self, input_words, lyrics_words):
        hannanum = Hannanum()
        vector1 = np.ones(len(lyrics_words))
        vector2 = np.zeros(len(lyrics_words))
        is_zero = True

        print("가사 배열: ", lyrics_words)
        print("매칭된 단어: ", end='')
        for i in input_words:
            for j in range(len(lyrics_words)):
                if i == lyrics_words[j]:
                    vector2[j] = 1
                    print(lyrics_words[j], end=' ')
                    is_zero = False
                    break
        print()
        if is_zero:
            return 0.0

        return self.cosine_similarity(vector1, vector2)

    # 노래 가사 중 유사도가 가장 높은 노래의 song_id 반환
    def max_similarity(self):
        konlpy = Hannanum()
        l = konlpy.nouns(self.lyrics_input)
        lyrics_list = self.lyrics_list
        song_id = 0
        max_similarity = 0.0

        result = self.compare_lyrics(self.lyrics_input)
        if result > 0:
            return result

        print("입력된 가사의 단어 배열: ", l)
        for lyrics in lyrics_list:
            if lyrics['words'] is None:
                lyrics['words'] = konlpy.nouns(lyrics['lyrics'])

            print("song_id, title: ", lyrics['song_id'], lyrics['title'])
            temp = self.measure_similarity(l, lyrics['words'])
            print("코사인 유사도: ", temp)
            print()
            if temp > max_similarity:
                song_id = lyrics['song_id']
                max_similarity = temp

        return song_id


if __name__ == '__main__':
    # test
    # 원 가사: 밤하늘의 별을 따서 너에게 줄래
    lyrics_input = '밤하늘의 별을 따서 너에게 줄래'
    db = DbConnector()
    song_list = db.select_ballad(10)
    for i in range(len(song_list)):
        song_list[i]['words'] = song_list[i]['words'].split()

    lf = LyricsFind(lyrics_input, song_list)
    start = time.time()
    print('lyrics input: ', lyrics_input)
    print(lf.max_similarity())
    print('lyrics find time (10 songs):', round(time.time() - start, 4), 'sec')