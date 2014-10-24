# Dockerfile for krakendash
#
# run this handing it a directory with a ceph.conf file and keys that are needed:
#
# docker run -i -t -v /etc/ceph:/etc/ceph -p 8000:8000 karcaw/krakendash
#
# Find out more about docker here: www.docker.com

FROM ubuntu:trusty

MAINTAINER karcaw@gmail.com


RUN apt-get update
RUN apt-get install -y python-pip python-dev libxml2-dev libxslt-dev zlib1g-dev
RUN apt-get install -y ceph screen 

ADD . /app
RUN cd /app/ && pip install -r requirements.txt

VOLUME /etc/ceph
EXPOSE 8000

CMD /app/contrib/startall.sh
