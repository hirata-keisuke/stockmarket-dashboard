FROM python:3.8-slim

RUN apt update -y\
    && apt upgrade -y\
    && apt install -y sqlite3

RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install -r reqirements.txt