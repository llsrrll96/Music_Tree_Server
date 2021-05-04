from numpy import dot
from numpy.linalg import norm
import numpy as np
from konlpy.tag import Kkma

# ex)
# lyrics_input : '니 손 꼭 잡고 그냥 이 길을 걸었으면 내게'
# lyrics_list : [{'song_id':1, 'words':['a', 'b', 'c']}, {'song_id':2, 'words':['b', 'c', 'd']}, ...]

class LyricsFind:
	def __init__(self, lyrics_input, lyrics_list):
		self.lyrics_input = lyrics_input
		self.lyrics_list = lyrics_list


	def compare_lyrics(self, lyrics):
		for l in self.lyrics_list:
			if lyrics == l:
				return True

		return False


	def cosine_similarity(self, a, b):
		return (dot(a, b) / (norm(a) * norm(b)))


# 노래 가사와 입력된 가사의 코사인 유사도 측정 후 유사도 반환
	def measure_similarity(self, lyrics, lyrics_words):
		konlpy = Kkma()
		vector1 = np.ones(len(lyrics_words))
		vector2 = np.zeros(len(lyrics_words))
		is_zero = True
		
		for i in lyrics:
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
		song_id = 1
		max_similarity = 0.0

		for lyrics in lyrics_list:
			print(lyrics['words'])
			temp = self.measure_similarity(l, lyrics['words'])
			print(lyrics['song_id'])
			if temp > max_similarity:
				song_id = lyrics['song_id']
				max_similarity = temp
		
		return song_id
			

if __name__ == '__main__':
	# test
	lf = LyricsFind('a', [{'words':['a', 'b', 'c'], 'song_id':123 }])
	print(lf.max_similarity())
