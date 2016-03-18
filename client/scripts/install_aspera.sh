#!/bin/bash

set -e
set -x

cd "$HOME"

# Download and verify Aspera Connect
# http://downloads.asperasoft.com/en/downloads/8?list
wget "http://download.asperasoft.com/download/sw/connect/3.6.1/aspera-connect-3.6.1.110647-linux-64.tar.gz"
echo "8069029bb307f56e8fae811148f076ac9a1f0edf  aspera-connect-3.6.1.110647-linux-64.tar.gz" | sha1sum -c -
tar -zxf aspera-connect-3.6.1.110647-linux-64.tar.gz

# Install Aspera Connect
# http://download.asperasoft.com/download/docs/connect/3.6.1/user_linux/webhelp/index.html#dita/installation.html
./aspera-connect-3.6.1.110647-linux-64.sh

rm aspera-connect-3.6.1.110647-linux-64.tar.gz
rm aspera-connect-3.6.1.110647-linux-64.sh

# Add path entry
cat >> "$HOME/.bashrc" <<EOF

export PATH=\$PATH:\$HOME/.aspera/connect/bin

EOF

echo "Finished installing"
echo "To use Aspera in this shell..."
echo "$ export PATH=\$PATH:\$HOME/.aspera/connect/bin"
