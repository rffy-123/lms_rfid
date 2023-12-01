from App.Admin import Admin
import hashlib  # Import hashlib for secure password hashing

class AdminManager():
    def __init__(self, DAO):
        self.admin = Admin(DAO.db.admin)
        self.user = DAO.db.user
        self.dao = self.admin.dao

    def signin(self, email, password):
            admin = self.dao.getByEmail(email)
            if admin is None:
                return False
            
            admin_pass = admin["password"]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if admin_pass != hashed_password:
                return False
            return admin
        
    def get(self, id):
        admin = self.dao.getById(id)
        return admin

    def getUsersList(self):
        admin = self.user.list()
        print(admin)
        return admin

    def signout(self):
        self.admin.signout()

    def user_list(self):
        return self.user.list()

    def add_admin(self, email, password):
        existing_admin = self.dao.getByEmail(email)
        if existing_admin:
            return "email_exists"

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        new_admin_info = {"email": email, "password": hashed_password}
        new_admin = self.dao.add(new_admin_info)
        return new_admin
    
