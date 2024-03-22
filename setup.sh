#!/bin/sh
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
dropdb capstone
createdb capstone
export FLASK_APP=flaskr
flask run