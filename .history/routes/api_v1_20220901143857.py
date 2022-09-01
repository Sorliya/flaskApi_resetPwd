# -*- coding: utf-8 -*-
from flask_restful import Api
from app import app
from app import api
from resources import user

api.add_resource(user.UserApi, "/user")
api.add_resource(user.LoginApi, '/auth')

api.add_resource(user.ForgotPassword, '/api/auth/forgot')
api.add_resource(user.ResetPassword, '/api/auth/reset')