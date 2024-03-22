
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Actor, Movie

class CapstoneTestCase(unittest.TestCase):

    """This class represents the capstone test case"""
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}/{}".format("localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Authentication Tokens Information
        with open('auth_config.json', 'r') as f:
            self.auth = json.loads(f.read())

        assistant_jwt = self.auth["roles"]["Casting Assistant"]["jwt_token"]
        director_jwt = self.auth["roles"]["Casting Director"]["jwt_token"]
        producer_jwt = self.auth["roles"]["Executive Producer"]["jwt_token"]
        self.auth_headers = {
            "Casting Assistant": f'Bearer {assistant_jwt}',
            "Casting Director": f'Bearer {director_jwt}',
            "Executive Producer": f'Bearer {producer_jwt}'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """Testing actors can be retrieved from database."""
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["actors"]))


    """Testing movies can be retrieved from database."""
    def test_retrieve_movies(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["movies"]))

     """Testing deletion of actor from database - covering success
     and failures on 422 and unauthorized"""
    def test_delete_actor_success(self):
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        res = self.client().delete("/actors/3", headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["id"], 3)

    def test_delete_actor_not_authorized(self):
        header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }

        res = self.client().delete("/actors/10", headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_delete_actor_does_not_exist(self):
        
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }

        res = self.client().delete("/actors/10", headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

     """Testing deletion of movies from database - covering success
     and failures on 422 and unauthorized"""
    def test_delete_movie_success(self):
        header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().delete("/movies/2", headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["id"], 2)

    def test_delete_movie_does_not_exist(self):
        header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().delete("/movies/10", headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_delete_movie_not_authorized(self):
        header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().delete("/movies/10", headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

     """Testing addition of actors from database - covering success
     and failure on 422 and unauthorized"""
    def test_add_actor_database_failure(self):
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        new_actor = {
            "age": "47",
            "gender":"FEMALE"
        }

        res = self.client().post("/actors", json=new_actor, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_add_actor_not_authorized(self):
        header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        new_actor = {
            "name": "Reese Witherspoon",
            "age": "47",
            "gender":"FEMALE"
        }

        res = self.client().post("/actors", json=new_actor, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_add_actor_success(self):
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }

        new_actor = {
            "name": "Reese Witherspoon",
            "age": "47",
            "gender":"FEMALE"
        }

        res = self.client().post("/actors", json=new_actor, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

     """Testing addition of moviesfrom database - covering success
     and failure on 422 and unauthorized"""
    def test_add_movie_success(self):
        header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }

        new_movie = {
             "release_date": "Fri, 11 Oct 2024 00:00:00 GMT",
            "title": "Piece by Piece"
        }

        res = self.client().post("/movies", json=new_movie, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_add_movie_database_fail(self):
        header = {
            "Authorization": self.auth_headers["Executive Producer"]
        }

        new_movie = {
             "release_date": "Fri, 11 Oct 2024 00:00:00 GMT",
        }

        res = self.client().post("/movies", json=new_movie, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_add_movie_unauthorized(self):
        header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }

        new_movie = {
             "release_date": "Fri, 11 Oct 2024 00:00:00 GMT",
            "title": "Piece by Piece"
        }

        res = self.client().post("/movies", json=new_movie, headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

     """Testing update of actors from database - covering success
     and failure on unauthorized"""
    def test_update_actor(self):
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }

        res = self.client().patch(f'/actors/1', json={'name': 'Updated Test Actor'}, headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_update_actor_unauthorized(self):
        header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }

        res = self.client().patch(f'/actors/1', json={'name': 'Updated Test Actor'}, headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    """Testing update of movies from database - covering success
     and failure on unauthorized"""
    def test_update_movie_success(self):
        header = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        new_movie = Movie(title='Test Movie', release_date='2024-03-19')
        new_movie.insert()

        res = self.client().patch(f'/movies/{new_movie.id}', json={'title': 'Updated Test Movie'}, headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])
        
    def test_update_movie_unauthorized(self):
        header = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }

        res = self.client().patch('/movies/1', json={'title': 'Updated Test Movie'}, headers=header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


