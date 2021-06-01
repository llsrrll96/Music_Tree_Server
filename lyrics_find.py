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
            print(l['lyrics'])
            if l['lyrics'].find(lyrics) != -1:
                return True

        return False

    def cosine_similarity(self, a, b):
        return dot(a, b) / (norm(a) * norm(b))

    # 노래 가사와 입력된 가사의 코사인 유사도 측정 후 유사도 반환
    def measure_similarity(self, lyrics, lyrics_words):
        hannanum = Hannanum()
        input_words = hannanum.nouns(lyrics)
        vector1 = np.ones(len(lyrics_words))
        vector2 = np.zeros(len(lyrics_words))
        is_zero = True

        for i in input_words:
            for j in range(len(lyrics_words)):
                if i == lyrics_words[j]:
                    vector2[j] = 1
                    is_zero = False
                    break

        if is_zero:
            return 0.0

        return self.cosine_similarity(vector1, vector2)

    # 노래 가사 중 유사도가 가장 높은 노래의 song_id 반환
    def max_similarity(self):
        l = self.lyrics_input
        lyrics_list = self.lyrics_list
        hannanum = Hannanum()
        song_id = 1
        max_similarity = 0.0

        for lyrics in lyrics_list:
            if lyrics['words'] is None:
                lyrics['words'] = hannanum.nouns(lyrics['lyrics'])

            temp = self.measure_similarity(l, lyrics['words'])

            if temp > max_similarity:
                song_id = lyrics['song_id']
                max_similarity = temp

        return song_id


if __name__ == '__main__':
    # test
    lyrics = '밤하늘의 별을 따서 너에게 줄래 너는 내가 사랑하니까 더 소중하니까 오직 너 아니면 안 된다고 외치고 싶어 그저 내 곁에만 있어줘 떠나지 말아줘 참 많이 어색했었죠 널 처음 만난 날 ' \
             '멀리서 좋아하다가 들킨 사람처럼 숨이 가득 차올라서 아무 말 하지 못했는데 너는 말 없이 웃으며 내 손 잡아줬죠 '
    lf = LyricsFind('밤하늘에 별을',
                    [{'words': None, 'song_id': 1, 'lyrics': lyrics}, {'words': None, 'song_id': 124, 'lyrics': lyrics},
                     {'words': None, 'song_id': 125, 'lyrics': lyrics}])
    start = time.time()
    print('start: ', start)
    print(lf.max_similarity())
    print(lf.compare_lyrics('a'))
    print('end: ', (time.time() - start))