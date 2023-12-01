
class UserDAO:
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "users"

    def list(self):
        users = self.db.query("select @table.id,@table.rfid,@table.name,@table.email,@table.bio,@table.mob,@table.lock,@table.created_at,count(reserve.book_id) as books_owned from @table LEFT JOIN reserve ON reserve.user_id=@table.id GROUP BY reserve.user_id").fetchall()
        return users

    def getById(self, id):
        q = self.db.query("select * from @table where id='{}'".format(id))
        user = q.fetchone()
        return user

    def getUsersByBook(self, book_id):
        q = self.db.query("select * from @table LEFT JOIN reserve ON reserve.user_id = @table.id WHERE reserve.book_id={}".format(book_id))
        user = q.fetchall()
        return user

    def getByEmail(self, email):
        q = self.db.query("select * from @table where email='{}'".format(email))
        user = q.fetchone()
        return user
    
    def getByRFID(self, rfid):
        q = self.db.query("SELECT * FROM @table WHERE rfid='{}'".format(rfid))
        user = q.fetchone()
        return user
    
    def add(self, user):
        rfid = user['rfid']  # Get RFID from the user dictionary
        name = user['name']
        email = user['email']
        password = user['password']

        # Update the SQL query to include the RFID field
        q = self.db.query("INSERT INTO @table (rfid, name, email, password) VALUES('{}', '{}', '{}', '{}');".format(rfid, name, email, password))
        self.db.commit()
        return q

    def update(self, user, _id):
        rfid = user['rfid']  # Get RFID from the user dictionary
        name = user['name']
        email = user['email']
        password = user['password']
        bio = user['bio']

        # Update the SQL query to include the RFID field
        q = self.db.query("UPDATE @table SET rfid='{}', name='{}', email='{}', password='{}', bio='{}' WHERE id={}".format(rfid, name, email, password, bio, _id))
        self.db.commit()
        return q
