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
RUN apt-get install -y libpng-dev libfreetype6-dev # matplotlib
RUN apt-get install -y swig # M2crypto
RUN apt-get install -y libsasl2-dev  libldap2-dev # python-ldap
RUN apt-get install -y libgeos-dev # Shapely
RUN apt-get install -y libmemcached-dev # pylibmc
RUN apt-get install -y libmysqlclient-dev # tiddlywebplugins.tiddlyspace
RUN apt-get install -y freetds-dev # pymssql
RUN apt-get install -y hdf5-tools libhdf5-dev # h5py
RUN apt-get install -y libblas-dev liblapack-dev gfortran # numpy
RUN apt-get install -y locales apt-utils ncurses-term

# Matplotlib. See https://github.com/matplotlib/matplotlib/issues/3029
RUN apt-get install -y libfreetype6-dev
RUN apt-get install -y pkg-config
RUN ln -s /usr/include/freetype2/ft2build.h /usr/include/

WORKDIR /root
ARG PYPY2_PACKAGE_URL=https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-7.0.0-linux_x86_64-portable.tar.bz2
ARG PYPY3_PACKAGE_URL=http://buildbot.pypy.org/nightly/py3.6/pypy-c-jit-latest-linux64.tar.bz2

RUN wget ${PYPY2_PACKAGE_URL} -nv -O - | tar xj
RUN ln -s $(python -c 'import os; print(os.path.basename(os.environ["PYPY2_PACKAGE_URL"]).rsplit(".", 2)[0])') pypy2_install
RUN pypy2_install/bin/virtualenv-pypy pypy2_venv

RUN wget ${PYPY3_PACKAGE_URL} -nv -O pypy.tar.bz2
RUN mkdir -p pypy3_install
RUN (cd pypy3_install; tar --strip-components=1 -xf ../pypy.tar.bz2)
RUN pypy3_install/bin/pypy3 -mensurepip
RUN pypy3_install/bin/pypy3 -mpip install --upgrade pip setuptools
RUN pypy3_install/bin/pypy3 -mpip install virtualenv
RUN pypy3_install/bin/virtualenv pypy3_venv
RUN pypy3_venv/bin/pip install numpy

RUN echo "source pypy3_venv/bin/activate" >> ~/.bashrc
RUN locale-gen en_US.UTF-8
RUN echo "export LANG=en_US.UTF-8" >> ~/.bashrc
RUN echo "export LANGUAGE=en_US.UTF-8" >> ~/.bashrc
RUN echo "export LC_ALL=en_US.UTF-8" >> ~/.bashrc
RUN echo "export LC_CTYPE=en_US.UTF-8" >> ~/.bashrc
