# pull official base image
FROM ubuntu:18.04

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV TZ=Asia/Singapore 
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install psycopg2 dependencies

RUN apt-get update && apt-get install -y \
    curl \
    python3-pip\
    python3-dev \
    libpq-dev \
    postgresql \
    postgresql-contrib \
    nginx

# install dependencies
#RUN pip install --upgrade pip

COPY ./requirements4.txt /usr/src/app/requirements4.txt
RUN pip3 install -r requirements4.txt

# copy project
COPY . /usr/src/app/
