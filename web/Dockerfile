FROM python:3.10

LABEL author=nurijusha version=1 mood=wtf

WORKDIR /code
COPY . .
RUN pip3 install --upgrade pip && pip3 install -r /code/requirements.txt
CMD gunicorn web.wsgi:application --bind 0.0.0.0:8000