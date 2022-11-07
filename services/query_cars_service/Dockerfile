# Dockerfile

# pull the official docker image
FROM python:3.9.6-slim-buster

# set work directory
WORKDIR /services/query_cars_service/

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt /services/query_cars_service/requirements.txt
RUN apt-get update -y && apt-get install -y build-essential libpq-dev &&\
    pip install --upgrade pip &&\
    pip install psycopg2-binary --no-binary psycopg2-binary &&\
    pip install -r /services/query_cars_service/requirements.txt \
    && rm -rf /root/.cache/pip 

# copy project
COPY . /services/query_cars_service