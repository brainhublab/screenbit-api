#!/bin/ash

if [ "$screenbit_ENV" = "production" ]; then
    echo Production env
    chown -R apache:root /usr/src/screenbitApi/server_media

    """
    change static folder permissions while debug = True in django settings
    othervise change only collected_static folder permission
    """
    chown -R apache:root /usr/src/screenbitApi/static
    chown -R apache:root /usr/src/screenbitApi/collected_static
    httpd -D FOREGROUND
else
    echo Developement env
    python manage.py runserver "0.0.0.0:${SCREENBIT_API_PORT}"
fi
