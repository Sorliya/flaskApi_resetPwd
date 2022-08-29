from .db import db

class Movie(db.Model):
    name = db.Column(db.String, required=True, unique=True)
    casts = db.Column(db.String, required=True)
    genres = db.Column(db.String, required=True)