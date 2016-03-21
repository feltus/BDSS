#!/usr/bin/env bash

set -e
set -x

# Install up to date version of pip
wget "https://bootstrap.pypa.io/get-pip.py"
python3 ./get-pip.py
rm -f get-pip.py

cd /vagrant
python3 setup.py develop

# Configure BDSS to talk to metadata repository on host machine
cat > /home/vagrant/.bdss.cfg <<EOF
[metadata_repository]
url=http://10.0.2.2:5000
EOF
