FROM python:3.7.4-alpine3.9
ENV PYTHONUNBUFFERED 1

RUN mkdir /usr/src/screenbitApi
COPY requirements.txt /usr/src/screenbitApi
WORKDIR /usr/src/screenbitApi


RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    && apk add apache2 \
    && apk add apache2-dev \
    && pip install -r requirements.txt \
    && pip install mod_wsgi \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps \
    && apk add --update ffmpeg

RUN mod_wsgi-express module-config >> /etc/apache2/httpd.conf

ENV screenbit_ENV=development

COPY ./screenbit.conf /etc/apache2/conf.d
COPY . /usr/src/screenbitApi

RUN apk add --no-cache tzdata
ENV TZ Europe/Sofia

CMD ./run.sh
