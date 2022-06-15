FROM python:3.9

LABEL author=nurijusha version=1 mood=wtf

WORKDIR /code
COPY ./app .
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip && pip3 install -r /code/requirements.txt
EXPOSE 6001