from flask import Flask, jsonify, Response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from sqlalchemy import asc
from config import Config
from models import db
from models.user import User
from flask_mail import Mail

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db.init_app(app)
app.app_context().push()
db.create_all()
from routes import api_v1
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)