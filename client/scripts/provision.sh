#!/usr/bin/env bash

set -e

apt-get update

# Install pip
wget "https://bootstrap.pypa.io/get-pip.py"
python3 ./get-pip.py

# Download and verify Aspera Connect
# http://downloads.asperasoft.com/en/downloads/8?list
wget "http://download.asperasoft.com/download/sw/connect/3.6.1/aspera-connect-3.6.1.110647-linux-64.tar.gz"
echo "8069029bb307f56e8fae811148f076ac9a1f0edf aspera-connect-3.6.1.110647-linux-64.tar.gz" | sha1sum -c -
tar -zxf aspera-connect-3.6.1.110647-linux-64.tar.gz

# Install Aspera Connect
# http://download.asperasoft.com/download/docs/connect/3.6.1/user_linux/webhelp/index.html#dita/installation.html
# Aspera cannot be installed as root
su - vagrant -c ./aspera-connect-3.6.1.110647-linux-64.sh

# Add path entry
cat >> $HOME/.bashrc <<EOF

export PATH=\$PATH:$HOME/.aspera/connect/bin
EOF

# Configure BDSS to talk to metadata repository on host machine
cat > $HOME/.bdss.cfg <<EOF
[metadata_repository]
url=http://10.0.2.2:5000
EOF
