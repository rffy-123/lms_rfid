import pymysql.cursors

class DB(object):
    host = "localhost"
    user = "root"
    password = ""
    db = "lms"
    table = ""

    def __init__(self, app):
        app.config["MYSQL_DATABASE_HOST"] = self.host
        app.config["MYSQL_DATABASE_USER"] = self.user
        app.config["MYSQL_DATABASE_PASSWORD"] = self.password
        app.config["MYSQL_DATABASE_DB"] = self.db

        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            cursorclass=pymysql.cursors.DictCursor
        )

    def cur(self):
        return self.connection.cursor()

    def query(self, q):
        with self.connection.cursor() as cursor:
            if len(self.table) > 0:
                q = q.replace("@table", self.table)
            cursor.execute(q)
        return cursor

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
