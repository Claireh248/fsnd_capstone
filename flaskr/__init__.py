import os
from flask import (
    Flask, 
    request, 
    abort, 
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from auth.auth import AuthError, requires_auth
from models import Actor, Movie, setup_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

        # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response


    #ROUTES

    '''
    Endpoint which fetches all actor data
    '''
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'Welcome to my Capstone API!' 
        })

    '''
    Endpoint which fetches all actor data
    '''
    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = Actor.query.all()
        return jsonify({
            'success': True, 
            'actors': [actor.format() for actor in actors]
        })

    '''
    Endpoint which fetches all movie data
    '''
    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })

    '''
    Endpoint which adds an actor to the database
    params: name, age & gender
    requires_auth: needs to be Executive Producer or Casting Director
    '''
    @app.route('/actors', methods=["POST"])
    @requires_auth('create:actor')
    def create_actor(payload):
        body = request.get_json()
        
        new_name = body.get("name")
        new_age = body.get("age")
        new_gender = body.get("gender")

        try:
            new_actor = Actor(name = new_name, age=new_age, gender=new_gender)
            new_actor.insert()

            return jsonify({
            "success": True, 
            "actor" : new_actor.format()
            })
        
        except Exception as e:
            print(e)
            abort(422)
        
        else:
            abort(422)


    '''
    Endpoint which adds a movie to the database
    params: title & release date
    requires_auth: needs to be Executive Producer
    '''
    @app.route('/movies', methods=["POST"])
    @requires_auth('create:movie')
    def create_movie(payload):
        body = request.get_json()
        
        new_title= body.get("title")
        new_release_date = body.get("release_date")

        try:
            new_movie = Movie(title=new_title, release_date=new_release_date)
            new_movie.insert()

            return jsonify({
            "success": True, 
            "actor" : new_movie.format()
            })
        
        except Exception as e:
            print(e)
            abort(422)
        else:
            abort(422)

    '''
    Endpoint which deletes an actor fromthe database
    params: id of actor to be deleted
    requires_auth: needs to be Casting Director or Executive Producer
    '''
    @app.route('/actors/<int:id>', methods=["DELETE"])
    @requires_auth('delete:actor')
    def delete_actor(payload, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        try:
            actor.delete()
            return jsonify(
            {
                "success": True,
                "id": id
            }
            )

        except Exception as e:
            print(e)
            abort(422)

    '''
    Endpoint which deletes a movie from the database
    params: id of movie to be deleted
    requires_auth: needs to be Executive Producer
    '''
    @app.route('/movies/<int:id>', methods=["DELETE"])
    @requires_auth('delete:movie')
    def delete_movie(payload, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        try:
            movie.delete()
            return jsonify(
            {
                "success": True,
                "id": id
            }
            )
        except Exception as e:
            print(e)
            abort(422)

    '''
    Endpoint which updates an actor on the database
    params: id of actor to be updated
    requires_auth: needs to be Casting Director or Executive Producer
    '''
    @app.route('/actors/<int:id>', methods=["PATCH"])
    @requires_auth('patch:actor')
    def patch_actor(payload, id):
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        try:
            if actor is None:
                abort(404)
            
            if body.get("name"):
                actor.name = body.get("name")

            if body.get("age"):
                actor.age = body.get("age")
            
            if body.get("gender"):
                actor.gender = body.get("gender")

            actor.update()

        except Exception as e:
            print(e)
            abort(400)
        
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    '''
    Endpoint which updates a movie on the database
    params: id of movie to be updated
    requires_auth: needs to be Casting Director or Executive Producer
    '''
    @app.route('/movies/<int:id>', methods=["PATCH"])
    @requires_auth('patch:movie')
    def patch_movie(payload, id):
        body = request.get_json()
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        try:
            if movie is None:
                abort(404)
            
            if body.get("title"):
                movie.title = body.get("title")

            if body.get("release_date"):
                movie.release_date = body.get("release_date")
            
            movie.update()

        except Exception as e:
            print(e)
            abort(400)
        
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200


    # Error Handling
    #error on database side
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    #Internal server error
    @app.errorhandler(500)
    def internal_server_error(error):
        return(
        jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500
        )

    #Not found error
    @app.errorhandler(404)
    def unauthorized(error):
        return(
        jsonify({
            "success": False,
            "error": 404,
            "message": 'Not Found'
        }), 404)

    #Invalid method
    @app.errorhandler(405)
    def method_not_allowed(error):
        return(
        jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed'
        }), 405)

    #Invalid method
    @app.errorhandler(401)
    def method_not_allowed(error):
        return(
        jsonify({
            "success": False,
            "error": 401,
            "message": 'Unauthorized'
        }), 401)

    #Method for authorisation errors
    @app.errorhandler(AuthError)
    def auth_error(error):
        return(
        jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()