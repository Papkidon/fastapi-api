# Dockerfile

# pull the official docker image
FROM python:3.9.6-slim-buster

# set working directory
WORKDIR /services/combined_cars_service

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt /services/combined_cars_service/requirements.txt
RUN apt-get update -y && apt-get -y install build-essential libpq-dev && \
    pip install --upgrade pip &&\
    pip install psycopg2-binary --no-binary psycopg2-binary &&\
    pip install -r /services/combined_cars_service/requirements.txt \
    && rm -rf /root/.cache/pip 

# copy project
COPY . /services/combined_cars_service