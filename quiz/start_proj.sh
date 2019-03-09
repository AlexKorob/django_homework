#!/bin/bash

python3 ./manage.py migrate

exec gunicorn -w 4 quiz.wsgi:application --bind 0.0.0.0:8000
