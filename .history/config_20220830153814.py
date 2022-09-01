import os

class Config(object):
    SECRET_KEY = 'A-VERY-LONG-SECRET-KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/jiangzihui/Downloads/flask/api_resetpwd/resetpwd.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = 'A-VERY-LONG-SECRET-KEY'

    #flask gmail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USERNAME='zihuijiang6@gmail.com'
    MAIL_PASSWORD='pbzqtegtdteugnhz'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USE_TLS=False
    