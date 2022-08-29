import os

class Config(object):
    SECRET_KEY = 'A-VERY-LONG-SECRET-KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/jiangzihui/Downloads/flask/api_resetpwd/resetpwd.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = 'A-VERY-LONG-SECRET-KEY'

    #flask gmail config
    MAIL_SERVER = 'yourmailserver'
    MAIL_USERNAME = 'yourmailusername'
    MAIL_PASSWORD = 'yourmailpassword' 
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False