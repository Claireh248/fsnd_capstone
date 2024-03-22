#!/bin/sh
sudo -u pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
sudo -u postgres dropdb capstone_test
sudo -u postgres createdb capstone_test
sudo -u postgres psql capstone_test < capstone.psql