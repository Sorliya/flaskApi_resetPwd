from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
#from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from models.user import User
import json

app = Flask(__name__)
api = Api(app)
db.init_app(app)
app.config.from_object(Config)

user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, help = "Username is required")
user_args.add_argument("password", type=str, help = "Password is required")
user_args.add_argument("email", type=str, help = "Email is required")

resource_fields = {
    'id': fields.Integer,
    "username": fields.String,
    "password": fields.String,
    "email": fields.String
}

class UserApi(Resource):
    @marshal_with(resource_fields)
    def get(self,id):
        result = User.query.filter_by(id=id).first()
        return result
    
    @marshal_with(resource_fields)
    def put(self,id):
        args = user_args.parse_args()
        result = User.query.filter_by(id=id).first()
        #if result:

        user = User(id=id, username=args['username'], password=args['password'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user,201

api.add_resource(UserApi, "/user")
        

if __name__ == '__main__':
    app.run(debug=True)