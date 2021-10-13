# Use an official Python image.
# https://hub.docker.com/_/python
FROM python:3.6-slim

WORKDIR /app
COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt
COPY database.ini /app/database.ini
COPY lib.py /app/lib.py

RUN pip3 install -r /app/requirements.txt

ENV PORT 80
ENV PYTHONUNBUFFERED TRUE

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --worker-class gthread app:app