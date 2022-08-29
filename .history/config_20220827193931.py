import os

class Config(object):
    SECRET_KEY = 'A-VERY-LONG-SECRET-KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/jiangzihui/Downloads/flask/api_resetpwd/resetpwd.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #flask gmail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'username@gmail.com'
    MAIL_PASSWORD = 'app password generated in step 3'