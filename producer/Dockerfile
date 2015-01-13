FROM python:2.7
MAINTAINER Jason Feinstein <jason@bandcamp.com>
ENV LAST_CHANGED 2015-01-13 4

RUN apt-get update 
RUN apt-get -y install python-pip git-core

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
CMD []