from flask import Response, request, render_template, url_for
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_restful.reqparse import RequestParser
from flask_mail import Message#, Mail
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from models import db
from sqlalchemy import asc, desc
import json
import datetime
from datetime import datetime, date, time, timedelta
from common.utils import *
from common.email import send_reset_password_mail, send_email
from models.user import User
from app import app, mail
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


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
        #verify = verify_hash(password=user_password, hash=db_password)
        
        if db_password != user_password:
            return Response(json.dumps({ 'msg': 'User and password does not match'}), mimetype='application/json')
        access_token = create_access_token(identity=args['email'])
        result = { 'access_token': access_token, 'username': data.username}
        
        return Response(json.dumps(result, cls=JSONEncoder), mimetype='application/json')
#第二种写法
class Login(Resource):
    def post(self):
        args = login_args.parse_args()
        user_password = args.get('password')
        user = User.query.filter(User.email == args['email']).first()
        authorized = user.check_password_hash(user_password)
        if not authorized:
            return Response(json.dumps({ 'msg': 'User is not exited'}), mimetype='application/json')

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200

forgot_args = login_args.copy()
class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'api/auth/reset/'
        args = request.get_json()
        #forgot_args.parse_args()
        email = args.get('email')
        if not email:
            return {'msg': 'Email input error'}
        user = User.query.filter(User.email == args['email']).first()
        if not user:
            return {'msg': 'This user does not exist'}
        expires = datetime.timedelta(hours=2)
        token = create_access_token(identity=args['email'], expires_delta=expires)#
        msg = Message('Confirm Email', sender='zihuijiang6@gmail.com', recipients=[email])
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = 'Your link is {}'.format(link)
        mail.send(msg)

        return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)

        '''return send_email('Reset Your Password',
                              sender='zihuijiang6@gmail.com',
                              recipients=[user.email],
                              html_body=render_template('email/reset_password.html',url=url + reset_token)
                            )'''
@app.route('/confirm_email/<token>')
def confirm_email(token):
    s = URLSafeTimedSerializer('Thisisasecret!')
    try:
        email = s.loads(token, max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    return '<h1>The token works!</h1>'
reset_parser = login_args.copy()
reset_parser.add_argument('reset_token')
class ResetPassword(Resource):
    def post(self):
        url = request.host_url + 'reset'
        try:
            args = reset_parser.parse_args()
            reset_token = args.get('reset_token')
            user_id = decode_token(reset_token)['identity']
            hashed_password = generate_hash(password=args.get('password'))
            with app.app_context():
                User.query.filter(User.id==user_id).update({
                        'username': args['username'], 
                        'password': hashed_password, 
                        'email': args['email']
                    })
                db.session.commit()
            '''if not reset_token or not password:
                return {'msg': 'Input error'}'''
            return send_email('Password reset successful',
                              sender='zihuijiang6@gmail.com',
                              recipients=[user.email],
                              html_body='<p>Password reset was successful</p>')
        except:
            return 
#向邮件发送token
#s = URLSafeTimedSerializer('Thisisasecret!')   
class SendMessageApi(Resource):
    def post(self):
        args = login_args.parse_args()
        email = args.get('email')
        user = User.query.filter(User.email == args['email']).first()
        token = user.generate_reset_password_token()
        result = send_reset_password_mail(user, token)
        # 验证是否发送成功
        if result is not None:
            return jsonify(msg='Mail sent successfully')
        else:
            return jsonify(msg='Email sending failed')