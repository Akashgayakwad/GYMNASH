FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get -y install binutils libproj-dev gdal-bin postgresql-client python3-lxml
RUN apt-get -y install libmemcached-dev

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/