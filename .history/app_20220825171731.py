from flask import Flask, jsonify, request

app = Flask(__name__)

movies = [
    {
        "id": 1,
        "name": "The Shawshank Redemption",
        "casts": ["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler"],
        "genres": ["Drama"]
    },
    {
        "id": 2,
       "name": "The Godfather ",
       "casts": ["Marlon Brando", "Al Pacino", "James Caan", "Diane Keaton"],
       "genres": ["Crime", "Drama"]
    }
]

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