import pymysql


class DbConnector:
    MYSQL_CONFIG = {
        'host': '119.56.229.177',
        'port': 3306,
        'user': 'test1',
        'password': '1234',
        'database': 'music_tree',
        'cursorclass': pymysql.cursors.DictCursor,
    }

    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(**self.MYSQL_CONFIG)

    def close(self):
        self.connection.close()

    # 예시 만들 때 사용
    def select_ballad(self, mood, n):
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                sql = 'SELECT * FROM music_tree.song WHERE genre = 1 AND mood = %s LIMIT %s'
                cursor.execute(sql, [mood, n])
                result = cursor.fetchall()
                return result
        finally:
            self.close()

    def select_all(self):
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                sql = 'SELECT * FROM music_tree.song'
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            self.close()


if __name__ == '__main__':
    db = DbConnector()
    print(db.select_ballad(5))