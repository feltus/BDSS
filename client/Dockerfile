FROM python:3.5.1-alpine

# Install BDSS client
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

# Install transfer mechanisms
RUN apk update
RUN apk upgrade
RUN apk add curl dropbear-scp
RUN rm -rf /var/cache/apk/*

# Aspera requires being run as a non-root user
RUN adduser -D bdss
WORKDIR /home/bdss

# Install Aspera
ENV aspera_version=3.6.1.110647-linux-64
RUN curl http://download.asperasoft.com/download/sw/connect/3.6.1/aspera-connect-${aspera_version}.tar.gz > aspera.tar.gz
RUN tar -zxf aspera.tar.gz
RUN su bdss -c ./aspera-connect-${aspera_version}.sh
RUN rm aspera.tar.gz
RUN rm ./aspera-connect-${aspera_version}.sh

# User, env, cwd for running client
USER bdss
WORKDIR /usr/src/app
ENV PATH="$PATH:/home/bdss/.aspera/connect/bin"

ENTRYPOINT ["python", "-m", "client"]
