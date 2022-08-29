from flask import Response, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_restful.reqparse import RequestParser
from models import db
from sqlalchemy import asc, desc
import json
from models.user import User
from app import app
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt)

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
    """Responsible for user registration
    """
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

    def put(self):
        user_args.add_argument("id", type=int, location='json', required=True)
        args = user_args.parse_args()
        #id=args.get('id')
        with app.app_context():
            user = User.query.filter(User.id==args['id']).update({
                'username': args['username'], 
                'password': args['password'], 
                'email': args['email']
                })
            db.session.commit()
        return Response(json.dumps({ 'msg': 'Update user successfully' }), status=200, mimetype='application/json')

