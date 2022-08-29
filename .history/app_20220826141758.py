from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import User

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config.from_object(Config)



if __name__ == '__main__':
    app.run(debug=True)