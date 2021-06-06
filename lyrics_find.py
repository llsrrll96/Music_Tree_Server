from numpy import dot
from numpy.linalg import norm
import numpy as np
from konlpy.tag import Kkma, Okt, Hannanum
import time
from db_connector import DbConnector


# ex)
# lyrics_input : '니 손 꼭 잡고 그냥 이 길을 걸었으면 내게'
# lyrics_list : [{'song_id':1, 'words':['a', 'b', 'c'], 'lyrics':'asdjklfasdkfj'}, {'song_id':2, 'words':['b', 'c', 'd'], 'lyrics':'zcvmzncv,msdlf'}, ...]

def df_to_dict(sub_list):
    for i in range(len(sub_list)):
        sub_list[i]['song_id'] = sub_list[i].pop('0')
        sub_list[i]['title'] = sub_list[i].pop('1')
        sub_list[i]['artist'] = sub_list[i].pop('2')
        sub_list[i]['album'] = sub_list[i].pop('3')
        sub_list[i]['ost'] = sub_list[i].pop('4')
        sub_list[i]['rel_date'] = sub_list[i].pop('5')
        sub_list[i]['genre'] = sub_list[i].pop('6')
        sub_list[i]['group_type'] = sub_list[i].pop('7')
        sub_list[i]['gender'] = sub_list[i].pop('8')
        sub_list[i]['feat'] = sub_list[i].pop('9')
        sub_list[i]['relevance'] = sub_list[i].pop('10')
        sub_list[i]['mood'] = sub_list[i].pop('11')
        sub_list[i]['lyrics'] = sub_list[i].pop('12')
        sub_list[i]['words'] = sub_list[i].pop('13')
        sub_list[i]['melon_song_id'] = sub_list[i].pop('14')

    return sub_list


class LyricsFind:
    def __init__(self, lyrics_input, song_list):
        self.lyrics_input = lyrics_input
        self.song_list = song_list

    def compare_lyrics(self):
        for song in self.song_list:
            if song['lyrics'] is not None and song['lyrics'].find(self.lyrics_input) != -1:
                print(song['song_id'], song['title'], '노래와 매칭됨')
                return song['song_id']

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
        song_list = self.song_list
        song_id = 0
        max_similarity = 0.0

        result = self.compare_lyrics()
        if result > 0:
            return result

        print("입력된 가사의 단어 배열: ", l)
        for song in song_list:
            if song['words'] is None:
                song['words'] = konlpy.nouns(song['lyrics'])

            print("song_id, title: ", song['song_id'], song['title'])
            temp = self.measure_similarity(l, song['words'])
            print("코사인 유사도: ", temp)
            print()
            if temp > max_similarity:
                song_id = song['song_id']
                # title 출력을 원한다면 주석해제
                # title = song['title']
                max_similarity = temp

        # title 출력을 원한다면 주석해제
        return song_id  # , title


if __name__ == '__main__':
    # test
    lyrics_input = '아침을 깨우는 니 생각에'
    db = DbConnector()
    # 1번째 인자: mood, 2번째 인자: limit
    song_list = db.select_ballad(8, 10)
    for i in range(len(song_list)):
        song_list[i]['words'] = song_list[i]['words'].split()

    lf = LyricsFind(lyrics_input, song_list)
    start = time.time()
    print('lyrics input: ', lyrics_input)
    print(lf.max_similarity())
    print('lyrics find time (10 songs):', round(time.time() - start, 4), 'sec')
