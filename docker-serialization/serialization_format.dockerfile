# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ARG FORMAT=proto
ARG ITERATIONS=100

COPY src src
COPY requirements.txt .

RUN pip3 install -r requirements.txt

# codegen
RUN python3 -m grpc_tools.protoc -I ./src/proto --python_out=./src/proto ./src/proto/user.proto

ENV FORMAT=${FORMAT}
ENV ITERATIONS=${ITERATIONS}

CMD python3 -m src.main --mode $FORMAT --port $PORT --iterations $ITERATIONS