# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt install default-jdk -y
RUN apt install mono-complete -y
RUN apt install timelimit -y 
COPY --chmod=700 . /code/
RUN mkdir /tmp/Solutions
RUN useradd --home /tmp/Solutions coder --shell /bin/bash

