FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /app/
WORKDIR /app
ADD . /app


RUN pip isntall -r requirements.txt


