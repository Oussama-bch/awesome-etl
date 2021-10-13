# Use an official Python image.
# https://hub.docker.com/_/python
FROM python:3.6-buster

WORKDIR /app

COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt
COPY database.ini /app/database.ini
COPY lib.py /app/lib.py
COPY etl_job.py /app/etl_job.py

RUN pip3 install -r /app/requirements.txt
ENV PYTHONUNBUFFERED TRUE

CMD ["app.py"]
ENTRYPOINT ["python3"]