# -*- coding: utf-8 -*-
from flask_restful import Api
from app import app, api
from resources import user

#api_v1 = Blueprint('api_v1', __name__)

api = Api(app)

api.add_resource(user.UserApi, "/user")
api.add_resource(user.LoginApi, '/auth')

api.add_resource(SignupApi, '/api/auth/signup')
        api.add_resource(LoginApi, '/api/auth/login')

        api.add_resource(ForgotPassword, '/api/auth/forgot')
        api.add_resource(ResetPassword, '/api/auth/reset')