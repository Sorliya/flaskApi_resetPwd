import os
from common.constant import *

class Config(object):
    SECRET_KEY = 'A-VERY-LONG-SECRET-KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/jiangzihui/Downloads/flask/api_resetpwd/resetpwd.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_BINDS = {
        "MASTER": SQL_CONNECTION_STR.format(
            db=os.environ[resetpwd.db]
        )
    }