class AdminDAO():
    db = {}

    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "admin"

    def getById(self, id):
        q = self.db.query("select * from @table where id='{}'".format(id))
        admin = q.fetchone()
        return admin

    def getByEmail(self, email):
        q = self.db.query("select * from @table where email='{}'".format(email))
        admin = q.fetchone()
        return admin

    def add(self, admin_info):
        email = admin_info['email']
        password = admin_info['password']

        q = self.db.query("INSERT INTO @table (email, password) VALUES('{}', '{}');".format(email, password))
        self.db.commit()

        return q
