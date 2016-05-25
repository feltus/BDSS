FROM python:3.5.1

# Install transfer mechanisms
RUN apt-get update \
    && apt-get install curl \
    && apt-get clean

# Install Aspera
# Aspera requires being run as a non-root user
RUN useradd --create-home bdss
WORKDIR /home/bdss
ENV aspera_version=3.6.1.110647-linux-64
ENV PATH="$PATH:/home/bdss/.aspera/connect/bin"
RUN curl http://download.asperasoft.com/download/sw/connect/3.6.1/aspera-connect-${aspera_version}.tar.gz > aspera.tar.gz \
    && tar -zxf aspera.tar.gz \
    && su bdss -c ./aspera-connect-${aspera_version}.sh \
    && rm aspera.tar.gz \
    && rm ./aspera-connect-${aspera_version}.sh

# Install vdb-validate from SRA Toolkit
WORKDIR /opt
ENV sratoolkit_version=2.6.2
RUN curl http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/${sratoolkit_version}/sratoolkit.${sratoolkit_version}-ubuntu64.tar.gz > sratoolkit.tar.gz \
    && tar -zxf sratoolkit.tar.gz \
    && rm sratoolkit.tar.gz \
    && find /opt/sratoolkit.${sratoolkit_version}-ubuntu64/bin -type f -o -type l | grep --invert-match 'vdb-validate' | xargs rm
ENV PATH="$PATH:/opt/sratoolkit.${sratoolkit_version}-ubuntu64/bin"

# Install BDSS client
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

# User, env, cwd for running client
USER bdss
ENTRYPOINT ["python", "-m", "client"]
