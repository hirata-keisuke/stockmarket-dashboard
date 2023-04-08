FROM python:3.8-slim

RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install pandas plotly dash scikit-learn xlrd yfinance pysqlite3

RUN sudo apt update \
    && sudo apt upgrade \
    && sudo apt install sqlite3