# syntax=docker/dockerfile:1
FROM python:3
EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt install default-jdk -y
RUN apt install mono-complete -y
RUN apt install nodejs -y
RUN apt install timelimit -y 
COPY --chmod=700 . /code/
RUN mkdir /tmp/Solutions
COPY readline.js /tmp/Solutions
COPY java.policy /tmp/Solutions
RUN useradd --home /tmp/Solutions coder --shell /bin/bash
WORKDIR "/tmp/Solutions"
RUN apt install npm -y
RUN npm install ts-node -y
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
