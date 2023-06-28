# syntax=docker/dockerfile:1
FROM python:slim-bullseye
WORKDIR /app
COPY ./mortalgold .
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt