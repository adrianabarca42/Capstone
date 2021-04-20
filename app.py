import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Actor, Movie

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  return app

db_drop_and_create_all()
APP = create_app()

@APP.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
  if not request.method == 'GET':
    abort(405)
  actors = Actor.query.all()
  if len(actors == 0):
    abort(404)
  try:
    return jsonify({
      'success': True,
      'actors': actors
    }), 200
  except:
    abort(422)


@APP.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
  if not request.method == 'GET':
    abort(405)
  movies = Movie.query.all()
  if len(movies == 0):
    abort(404)
  try:
    return jsonify({
      'success': True,
      'movies': movies
    }), 200

@APP.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(payload, id):
  if not request.method == 'DELETE':
    abort(405)
  actor = Actor.query.filter(Actor.id == id).one_or_none()
  if actor is None:
    abort(404)
  try:
    actor.delete()
    return jsonify({
      'success': True,
      'deleted': actor.id
    }), 200
  except:
    abort(422)

@APP.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(payload, id):
  if not request.method == 'DELETE':
    abort(405)
  movie = Movie.query.filter(Movie.id == id).one_or_none()
  if movie is None:
    abort(404)
  try:
    movie.delete()
    return jsonify({
      'success': True,
      'deleted': movie.id
    }), 200
  except:
    abort(422)

@APP.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actors(payload):
  if not request.method == 'POST':
    abort(405)
  body = request.get_json()
  name = body.get('name')
  age = body.get('age')
  gender = body.get('gender')
  new_actor = Actor(name=name, age=age, gender=gender)
  new_actor.insert()
  try:
    return jsonify({
      'success': True,
      'actor': new_actor.name
    }), 200
  except:
    abort(422)

@APP.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_actors(payload):
  if not request.method == 'POST':
    abort(405)
  body = request.get_json()
  title = body.get('title')
  release_date = body.get('release_date')
  actors = body.get('actors')
  new_movie = Movie(title=title, release_date=release_date, actors=actors)
  new_movie.insert()
  try:
    return jsonify({
      'success': True,
      'actor': new_movie.title
    }), 200
  except:
    abort(422)

@APP.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actors(payload, id):
  if not request.method == 'PATCH':
    abort(405)
  actor = Actor.query.filter(Actor.id == id).one_or_none()
  if actor is None:
    abort(404)
  body = request.get_json()
  name = body.get('name')
  age = body.get('age')
  gender = body.get('gender')
  actor.name = name
  actor.age = age
  actor.gender = gender
  actor.update()
  try:
    return jsonify({
      'success': True,
      'actor': actor.name
    }), 200
  except:
    abort(422)

@APP.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movies(payload, id):
  if not request.method == 'PATCH':
    abort(405)
  movie = Movie.query.filter(Movie.id == id).one_or_none()
  if movie is None:
    abort(404)
  body = request.get_json()
  title = body.get('title')
  release_date = body.get('release_date')
  actors = body.get('actors')
  movie.title = title
  movie.release_date = release_date
  movie.actors = actors
  movie.update()
  try:
    return jsonify({
      'success': True,
      'actor': movie.title
    }), 200
  except:
    abort(422)

## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                "success": False, 
                "error": 422,
                "message": "unprocessable"
                }), 422

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                "success": False, 
                "error": 404,
                "message": "resource not found"
                }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
                "success": False, 
                "error": 405,
                "message": "method not allowed"
                }), 405


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)