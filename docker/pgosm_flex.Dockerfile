FROM python:3.11

LABEL maintainer="sireesh"

ARG OSM2PGSQL_BRANCH="master"
ARG OSM2PGSQL_REPO=https://github.com/osm2pgsql-dev/osm2pgsql.git

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        sqitch wget ca-certificates \
        git make cmake g++ \
        libboost-dev libboost-system-dev \
        libboost-filesystem-dev libexpat1-dev zlib1g-dev \
        libbz2-dev libpq-dev libproj-dev lua5.4 liblua5.4-dev \
        python3 python3-distutils \
        curl unzip \
        nlohmann-json3-dev \
	osm2pgsql \
	osmium-tool \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://luarocks.org/releases/luarocks-3.9.2.tar.gz \
    && tar zxpf luarocks-3.9.2.tar.gz \
    && cd luarocks-3.9.2 \
    && ./configure && make && make install

RUN luarocks install inifile
RUN luarocks install luasql-postgres PGSQL_INCDIR=/usr/include/postgresql/

WORKDIR /tmp
RUN git clone --depth 1 --branch $OSM2PGSQL_BRANCH $OSM2PGSQL_REPO \
    && mkdir osm2pgsql/build \
    && cd osm2pgsql/build \
    && cmake .. -D USE_PROJ_LIB=6 \
    && make -j$(nproc) \
    && make install \
    && cd /tmp && rm -r /tmp/osm2pgsql

WORKDIR /app
COPY . ./

RUN pip install -r requirements.txt
