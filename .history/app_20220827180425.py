from flask import Flask, jsonify, Response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_bcrypt import Bcrypt
from sqlalchemy import asc
from config import Config
from models import db
from models.user import User

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db.init_app(app)
from routes import api_v1
bcrypt = Bcrypt(app)