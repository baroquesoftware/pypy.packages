FROM ubuntu

RUN apt-get -y update

RUN apt-get install -y software-properties-common
RUN apt-get install -y wget
RUN apt-get install -y gcc
RUN apt-get install -y pypy-dev

RUN apt-get install -y libxml2-dev
RUN apt-get install -y libssl-dev

RUN add-apt-repository ppa:pypy/ppa

RUN apt-get -y update

RUN apt-get install -y pypy

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN pypy get-pip.py

# docker run -v /vagrant/pippache:/pipcache pypyspace pypy -m pip --cache-dir=/pipcache install django
