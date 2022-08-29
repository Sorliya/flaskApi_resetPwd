from flask import Flask, jsonify, Response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc
from config import Config
from models import db
from models.user import User
import json

app = Flask(__name__)
api = Api(app)
db.init_app(app)
app.config.from_object(Config)

user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, location='json', required=True)
user_args.add_argument("password", type=str, location='json', required=True)
user_args.add_argument("email", type=str, location='json', required=True)

resource_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "password": fields.String,
    "email": fields.String
}

class UserApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        data = User.query.order_by(asc(User.id)).all()
        return data
    
    def post(self):
        args = user_args.parse_args()
        with app.app_context():
            user = User(username=args['username'], password=args['password'], email=args['email'])
            db.session.add(user)
            db.session.commit()
        return Response(json.dumps({ 'msg': 'Create user successfully' }), status=200, mimetype='application/json')


    @marshal_with(resource_fields)
    def put(self):
        user_args.add_argument("id", type=int, location='json', required=True)
        args = user_args.parse_args()
        id=
        with app.app_context():
            user = User(id=id, username=args['username'], password=args['password'], email=args['email'])
            db.session.commit()
        return Response(json.dumps({ 'msg': 'Update user successfully' }), status=200, mimetype='application/json')

api.add_resource(UserApi, "/user")
        

if __name__ == '__main__':
    app.run(debug=True)