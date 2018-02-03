FROM ubuntu

RUN apt-get -y update

RUN apt-get install -y software-properties-common
RUN apt-get install -y wget
RUN apt-get install -y gcc g++ make

RUN apt-get install -y libssl-dev
RUN apt-get install -y libxml2-dev libxslt-dev cython # lxml
RUN apt-get install -y libpq-dev # psycopg2
RUN apt-get install -y libjpeg-dev # pillow
RUN apt-get install -y libcurl4-openssl-dev # pycurl
RUN apt-get install -y libcups2-dev # pycups
RUN apt-get install -y libpng12-dev libfreetype6-dev # matplotlib
RUN apt-get install -y swig # M2crypto
RUN apt-get install -y libsasl2-dev  libldap2-dev # python-ldap
RUN apt-get install -y libgeos-dev # Shapely
RUN apt-get install -y libmemcached-dev # pylibmc
RUN apt-get install -y libmysqlclient-dev # tiddlywebplugins.tiddlyspace
RUN apt-get install -y freetds-dev # pymssql
RUN apt-get install -y hdf5-tools libhdf5-dev # h5py


RUN wget https://bitbucket.org/pypy/pypy/downloads/pypy-5.0.0-linux64.tar.bz2
RUN tar xvjf pypy-5.0.0-linux64.tar.bz2

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN pypy-5.0.0-linux64/bin/pypy get-pip.py
