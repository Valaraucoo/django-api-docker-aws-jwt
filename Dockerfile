FROM python:3.10.0a1-alpine3.12

COPY requirements.txt /app/requirements.txt

RUN set -ex \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
ADD . .

CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
