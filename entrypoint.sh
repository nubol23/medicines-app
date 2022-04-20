#!/bin/bash

echo "Applying migrations"
./manage.py migrate

echo "Starting server"
#./manage.py runserver 0.0.0.0:"$PORT"
gunicorn config.wsgi:application --bind 0.0.0.0:"$PORT"
