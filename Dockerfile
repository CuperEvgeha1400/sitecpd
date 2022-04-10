FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /app/
WORKDIR /app
ADD . /app


RUN pip isntall -r requirements.txt
RUN sudo service redis-server start
RUN celery -A config worker -l INFO


