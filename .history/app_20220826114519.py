from flask import Flask, jsonify, request
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

@app.route('/movies')
def hello():
    return jsonify(movies)

@app.route('/movies', methods=['POST'])
def add_movie():
    movie = request.get_json()
    movies.append(movie)
    return {'id': len(movies)}, 200

@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    movie = request.get_json()
    movies[id] = movie
    return jsonify(movies[id]), 200

@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movies.pop(id)
    return 'None', 200

app.run()