from .db import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), unique=True)
    casts = db.Column(db.String(5))
    genres = db.Column(db.String(5))

    def __init__(self,name,casts,genres):
        self.name = name
        self.casts = casts
        self.genres = genres