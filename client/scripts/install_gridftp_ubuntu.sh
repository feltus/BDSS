#!/bin/bash

set -e
set -x

# http://toolkit.globus.org/toolkit/docs/latest-stable/admin/install/#install-toolkit

wget "http://toolkit.globus.org/ftppub/gt6/installers/repo/globus-toolkit-repo_latest_all.deb"
dpkg -i "globus-toolkit-repo_latest_all.deb"
rm "globus-toolkit-repo_latest_all.deb"
apt-get --yes update

apt-get --yes install globus-gridftp
