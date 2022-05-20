FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y libpq-dev python3-dev build-essential

COPY . /app
RUN chmod -R +x /app/scripts

RUN pip install -r /app/requirements.txt

WORKDIR /app