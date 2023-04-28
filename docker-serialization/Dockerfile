# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY . .

RUN pip3 install -r requirements.txt

# codegen
RUN python3 -m grpc_tools.protoc -I proto --python-betterproto-out=./proto proto/user.proto