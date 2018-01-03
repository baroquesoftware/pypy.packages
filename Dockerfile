FROM ubuntu

ARG PYPY2_PACKAGE_URL=https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3.5-5.10.0-linux_x86_64-portable.tar.bz2
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
RUN apt-get install -y libblas-dev liblapack-dev gfortran
RUN apt-get install -y vim

WORKDIR /root

RUN wget ${PYPY2_PACKAGE_URL} -nv -O - | tar xj

RUN ln -s $(python -c 'import os; print(os.path.basename(os.environ["PYPY2_PACKAGE_URL"]).rsplit(".", 2)[0])') pypy_install
RUN pypy_install/bin/virtualenv-pypy pypy_venv
