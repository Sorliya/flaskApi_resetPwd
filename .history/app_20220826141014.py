from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import User
import json

app = Flask(__name__)
db = SQLAlchemy(app)

app.config.from_object(Config)

@app.route('/users', methods=['GET'])
def users():
    users = request.get_json()
    return jsonify(movies), 200

@app.route('/users/<int:id>', methods=['GET', 'PUT'])
def update_user(id):
    users = request.get_json()
    users[id] = user
    return jsonify(movies[id]), 200

if __name__ == '__main__':
    app.run(debug=True)