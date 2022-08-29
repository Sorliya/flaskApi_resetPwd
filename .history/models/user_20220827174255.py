from flask import current_app
from . import db
import jwt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def generate_reset_password_token(self):
        #这就是token
        return jwt.encode({"id": self.id}, current_app.config['SECRET_KEY'], algorithm="HS256")
        
    def check_password(self, password):
        return check_password_hash(self.password, password)