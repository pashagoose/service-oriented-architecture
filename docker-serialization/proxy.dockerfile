# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY src src
COPY requirements_proxy.txt .

RUN pip3 install -r requirements_proxy.txt

CMD python3 -m src.proxy