from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields
#from flask_sqlalchemy import SQLAlchemy
from config import Config
from models.user import User

app = Flask(__name__)
api = Api(app)
db.init_app(app)
app.config.from_object(Config)

user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, help = "Username is required")
user_args.add_argument("password", type=str, help = "Password is required")
user_args.add_argument("email", type=str, help = "Email is required")

'''resource_fields = {
    'id': fields.String(required)
}'''

class UserApi(Resource):
    def get(self, user_id):
        result = User.query.get(id=user_id)
        return result
    
    #def put(self, user_id):

api.add_resource(UserApi, "/user/<int:user_id>")
        

if __name__ == '__main__':
    app.run(debug=True)