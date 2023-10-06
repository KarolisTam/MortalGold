# syntax=docker/dockerfile:1
FROM python:3.11-slim-bullseye
WORKDIR /app
COPY ./mortalgold .
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt