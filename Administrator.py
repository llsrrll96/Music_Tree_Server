import db_connector


def song_modify(input):
    # input = [ 수정할 특성명, 넣을 데이터, 수정할 노래 id ]
    db = db_connector.DbConnector()
    db.connect()
    try:
        with db.connection.cursor() as cursor:
            sql = "update music_tree.song set {} = %s where id=%s;"
            sql = sql.format(input[0])  # 수정할 특성 명을 {}부분에 넣어줌
            del input[0]
            result = cursor.execute(sql, input)
            db.connection.commit()
            return result
    finally:
        db.close()


def song_delete(input):
    # input = 삭제할 노래 id
    db = db_connector.DbConnector()
    db.connect()
    try:
        with db.connection.cursor() as cursor:
            sql = "delete from music_tree.song where id='%s';"
            result = cursor.execute(sql, input)
            db.connection.commit()
            return result
    finally:
        db.close()


def song_inquiry(input):
    # input = 조회할 노래 시작점 ( 배열 인덱스 ) / 시작점부터 50곡 id 오름차순 정렬해 불러옴
    db = db_connector.DbConnector()
    db.connect()
    try:
        with db.connection.cursor() as cursor:
            sql = "SELECT * FROM music_tree.song order by id limit %s, 50;"
            cursor.execute(sql, input-1)
            result = cursor.fetchall()
            return result
    finally:
        db.close()


