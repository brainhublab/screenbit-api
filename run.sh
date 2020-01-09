#!/bin/ash

if [ "$screenbit_ENV" = "production" ]; then
    echo Production env
    python manage.py runserver "0.0.0.0:${screenbit_API_PORT}"
else
    echo Developement env
    python manage.py runserver "0.0.0.0:${screenbit_API_PORT}"
fi
