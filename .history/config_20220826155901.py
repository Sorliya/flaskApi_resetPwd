from common.constant import *

class Config(object):
    SECRET_KEY = 'A-VERY-LONG-SECRET-KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/jiangzihui/Downloads/flask/api_resetpwd/resetpwd.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_BINDS = {
        "MASTER": SQL_CONNECTION_STR.format(
            user=os.environ["DB_MASTER_USER"],
            pw=os.environ["DB_MASTER_PASSWORD"],
            url=os.environ["DB_MASTER_HOST"],
            port=os.environ["DB_MASTER_PORT"],
            db=os.environ["DB_MASTER_NAME"]
        )
    }