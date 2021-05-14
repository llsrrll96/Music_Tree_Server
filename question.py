# -*- coding: utf-8 -*-

# song_list를 사용자의 입력에 맞게 필터링
# 예) 클라이언트로부터 성별이 남성이라는 입력이 들어왔을 때,
# attribute : gender, value : 1(남성)으로 함수 인자 설정
def filter_song_list(song_list, attribute, value):
	result = []
	for i in song_list:
		if i[attribute] == value:
			result.append(i)
	return result


def create_question(socket_id):
	data = {
		"step" : "1",
		"q" : "1번 질문입니다.",
		"socketId" : socket_id
	}
	return data


if __name__ == '__main__':
	song_list = [{'song_id' : 100, 'gender' : 1, 'type' : 1}, {'song_id' : 123, 'gender' : 2, 'type' : 1}]
	print(filter_song_list(song_list, 'type', 1))
