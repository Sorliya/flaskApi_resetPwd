from flask import Response, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_restful.reqparse import RequestParser
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from models import db
from sqlalchemy import asc, desc
import json
import datetime
from datetime import datetime, date, time, timedelta
from common.utils import *
from models.user import User
from app import app, mail
from . import bcrypt

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
        hashed_password = generate_hash(password=args['password'])
        with app.app_context():
            user = User(username=args['username'], password=args['password'], email=args['email'])
            db.session.add(user)
            db.session.commit()
        return Response(json.dumps({ 'msg': 'Create user successfully' }), status=200, mimetype='application/json')

    def put(self):
        """Update existing user
        """
        user_args.add_argument("id", type=int, location='json', required=True)
        args = user_args.parse_args()
        hashed_password = generate_hash(password=args['password'])
        with app.app_context():
            if hashed_password != '':
                User.query.filter(User.id==args['id']).update({
                'username': args['username'], 
                'password': args['password'], 
                'email': args['email']
                })
            else:
                User.query.filter(User.id==args['id']).update({
                'username': args['username'], 
                'email': args['email']
                })
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return Response(json.dumps({ 'msg': 'Duplicate key already exists' }), mimetype='application/json')

        return Response(json.dumps({ 'msg': 'Update user successfully' }), status=200, mimetype='application/json')

login_args = reqparse.RequestParser()
login_args.add_argument("password", type=str, location='json', required=True)
login_args.add_argument("email", type=str, location='json', required=True)

class LoginApi(Resource):
    """User login management
    """
    def post(self):
        args = login_args.parse_args()
        data = User.query.filter(User.email == args['email']).first()
        if data.email==0:
            return Response(json.dumps({ 'msg': 'Email & password does not match' }), mimetype='application/json')
        db_password = data.password
        user_password = args.get('password')
        if db_password != user_password:
            return Response(json.dumps({ 'msg': 'User and password does not match'}), mimetype='application/json')
        token = create_access_token(identity=args['email'])
        result = { 'access_token': token, 'username': data.username}
        return Response(json.dumps(result, cls=JSONEncoder), mimetype='application/json')

s = URLSafeTimedSerializer('Thisisasecret!')
class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'api/auth/reset'
        args = request.get_json()
        email = args.get('email')
        if not email:
            return {'msg': 'Email input error'}
        user = User.query.filter(User.email == args['email']).first()
        if not user:
            return {'msg': 'This user does not exist'}
        token = s.dumps(email, salt='email-confirm')
        msg = Message('Confirm Email', sender='zihuijiang6@gmail.com', recipients=[email])
        msg.body = 'Your link is {}'.format(url)
        mail.send(msg)
        return {'token': token}

class ResetPassword(Resource):
    def post(self):
        body = request.get_json()
        token = body.get('token')
        password = body.get('password')
        user_email = s.loads(token, salt='email-confirm', max_age=3600)
        user = User.query.filter(User.email==user_email).first()
        user.password = password
        db.session.commit()
        return {'msg': 'Password reset was successful'}