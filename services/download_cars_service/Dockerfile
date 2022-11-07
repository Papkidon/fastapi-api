# Dockerfile

# pull the official docker image
FROM python:3.9.6-slim-buster

# set working directory
WORKDIR /services/download_cars_service

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt /services/download_cars_service/requirements.txt
RUN apt-get update -y &&\
    pip install -r /services/download_cars_service/requirements.txt &&\
    rm -rf /root/.cache/pip

# copy project
COPY . /services/download_cars_service