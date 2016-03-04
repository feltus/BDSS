# Aspera

## About

BDSS uses the `ascp` command line client that comes with [Aspera](http://asperasoft.com/) Connect.

* http://download.asperasoft.com/download/docs/ascp/3.5.2/html/index.html
* http://www.ncbi.nlm.nih.gov/books/NBK242625/

## Installation

* http://downloads.asperasoft.com/en/downloads/8?list
* http://download.asperasoft.com/download/docs/connect/3.6.1/user_linux/webhelp/index.html#dita/installation.html

```Shell
# Aspera Connect can only be installed per-user, not system wide, on Linux.
cd $HOME

# Download and verify installer.
echo "8069029bb307f56e8fae811148f076ac9a1f0edf  aspera-connect-3.6.1.110647-linux-64.tar.gz" | sha1sum -c -
tar -zxf aspera-connect-3.6.1.110647-linux-64.tar.gz

./aspera-connect-3.6.1.110647-linux-64.sh

# Add path entry
echo 'export PATH=$PATH:$HOME/.aspera/connect/bin' >> ~/.bashrc

# Cleanup
rm aspera-connect-3.6.1.110647-linux-64.tar.gz
rm aspera-connect-3.6.1.110647-linux-64.sh
```
