# Flask API Documentation

This API provides endpoints for managing actors and movies in a database. It requires authentication for certain operations based on user roles. This Project is part of the Full Stack Developer Nanodegree as part of Udacity.

## Installation

1. Create a virtual env using `python -m env`
2. run `source env/bin/activate`
3. Install the required packages using `pip install -r requirements.txt`.
4. Set up the database by running the database setup script.

## Usage

### Starting the Server Locally

To start the server, from the starter directory run:

```bash
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
createdb capstone
export FLASK_APP = flaskr
flask run
```

### Accessing Deployed Application

The application is currently deployed on `https://fsnd-capstone-pt6p.onrender.com`

This is the URL that is listed in the postman tests - the unit tests use a local database.

## Endpoints

### Get Actors

- **URL:** `/actors`
- **Method:** `GET`
- **Description:** Fetches all actors from the database.
- **Requires Authentication:** No
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
        "success": true,
        "actors": [ { "id": 1, "name": "Actor 1", "age": 30, "gender": "MALE" }, { "id": 2, "name": "Actor 2", "age": 25, "gender": "FEMALE" }, ... ]
    }
    ```

### Get Movies

- **URL:** `/movies`
- **Method:** `GET`
- **Description:** Fetches all movies from the database.
- **Requires Authentication:** No
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
        "success": true,
        "movies": [ { "id": 1, "title": "Movie 1", "release_date": "2023-01-01T00:00:00" }, { "id": 2, "title": "Movie 2", "release_date": "2024-03-15T00:00:00" }, ... ]
    }
    ```

### Create Actor

- **URL:** `/actors`
- **Method:** `POST`
- **Description:** Adds a new actor to the database.
- **Requires Authentication:** Yes (Executive Producer or Casting Director)
- **Parameters:**
  - `None`
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "success": true,
      "actor": { "id": 3, "name": "New Actor", "age": 40, "gender": "MALE" }
    }
    ```

### Create Movie

- **URL:** `/movies`
- **Method:** `POST`
- **Description:** Adds a new movie to the database.
- **Requires Authentication:** Yes (Executive Producer)
- **Parameters:**
  - `None`
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "success": true,
      "movie": {
        "id": 4,
        "title": "Movie",
        "release_date": "2022-12-25T00:00:00"
      }
    }
    ```

### Delete Actor

- **URL:** `/actors/<id>`
- **Method:** `DELETE`
- **Description:** Deletes an actor from the database.
- **Requires Authentication:** Yes (Casting Director or Executive Producer)
- **Parameters:**
  - `id` (integer): ID of the actor to delete.
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "success": true,
      "id": 3
    }
    ```

### Delete Movie

- **URL:** `/movies/<id>`
- **Method:** `DELETE`
- **Description:** Deletes a movie from the database.
- **Requires Authentication:** Yes (Executive Producer)
- **Parameters:**
  - `id` (integer): ID of the movie to delete.
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "success": true,
      "id": 4
    }
    ```

### Update Actor

- **URL:** `/actors/<id>`
- **Method:** `PATCH`
- **Description:** Updates an existing actor in the database.
- **Requires Authentication:** Yes (Casting Director or Executive Producer)
- **Parameters:**
  - `id` (integer): ID of the actor to update.
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "success": true,
      "actor": {
        "id": 3,
        "name": "Updated Actor",
        "age": 35,
        "gender": "FEMALE"
      }
    }
    ```

### Update Movie

- **URL:** `/movies/<id>`
- **Method:** `PATCH`
- **Description:** Updates an existing movie in the database.
- **Requires Authentication:** Yes (Casting Director or Executive Producer)
- **Parameters:**
  - `id` (integer): ID of the movie to update.
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "success": true,
      "movie": {
        "id": 4,
        "title": "Updated Movie",
        "release_date": "2023-07-10T00:00:00"
      }
    }
    ```

## Error Handling

- **422 Unprocessable Entity:** If there was an issue processing the request with the database.
- **500 Internal Server Error:** If there was an internal server error.
- **404 Not Found:** If the requested resource was not found.
- **405 Method Not Allowed:** If an unsupported method is used on an endpoint.
- **401 Unauthorized:** If the user is not authorized to access the endpoint.
- **403 Unauthorized:** If the user's role group is not allowed to access the endpoint.

### Testing

Ensure you have ran the following:

1. ./setup_tests.sh
2. python3 test_app.py

There is also a postman collection gathered which can be imported into postman - the bearer tokens for each role group is included in this.
