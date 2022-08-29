from . import db
import jwt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')
        
    def check_password(self, password):
        return check_password_hash(self.password, password)