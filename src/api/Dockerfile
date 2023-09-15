FROM python:3.11.5-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt 

COPY . . 


 