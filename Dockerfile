FROM python:3.7.3

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY static /code/
COPY manage.py /code/
COPY poller /code/
COPY app_poller /code/
