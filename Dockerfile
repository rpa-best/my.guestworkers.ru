FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app/

COPY /requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/