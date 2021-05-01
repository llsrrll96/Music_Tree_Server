from Music_Tree_Server import db_connector


def song_modify(input):
    # input = [ '가사', '관련성', '분위기', 수정할 노래 id ]
    db = db_connector.DbConnector()
    db.connect()
    try:
        with db.connection.cursor() as cursor:
            sql = "update music_tree.song set lyrics=%s,relevance=%s,mood=%s where songid=%s;"
            cursor.execute(sql, input)
            db.connection.commit()
    finally:
        db.close()


def song_delete(input):
    # input = 삭제할 노래 id
    db = db_connector.DbConnector()
    db.connect()
    try:
        with db.connection.cursor() as cursor:
            sql = "delete from music_tree.song where songid='%s';"
            cursor.execute(sql, input)
            db.connection.commit()
    finally:
        db.close()


def song_inquiry(input):
    # input = 조회할 노래 시작점 - 1 / 시작점부터 50곡 불러옴
    db = db_connector.DbConnector()
    db.connect()
    try:
        with db.connection.cursor() as cursor:
            sql = "SELECT * FROM music_tree.song limit %s, 50;"
            cursor.execute(sql, input)
            result = cursor.fetchall()
            print(result)
    finally:
        db.close()

