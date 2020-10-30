FROM python:3.6

RUN apt install libxml2-dev libxslt-dev
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./src .
