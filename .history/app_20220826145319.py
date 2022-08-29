from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields
#from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from models.user import User


app = Flask(__name__)
api = Api(app)
db.init_app(app)
app.config.from_object(Config)

user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, help = "Username is required")
user_args.add_argument("password", type=str, help = "Password is required")
user_args.add_argument("email", type=str, help = "Email is required")

resource_fields = {
    'id': fields.Integer
}

class UserApi(Resource):
    def get(self):
        args = user_args.parse_args()
        username = args.get('username')
        password = args.get('password')
        email = args.get('email')
        #result = User.query.get(id=id)
        return jsonify(status=200, msg = 'ok')
    
    #def put(self, user_id):

api.add_resource(UserApi, "/user")
        

if __name__ == '__main__':
    app.run(debug=True)