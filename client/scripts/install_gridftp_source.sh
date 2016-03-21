#!/bin/bash

set -e
set -x

# The directory where the Globus Toolkit will be installed.
INSTALL_DIR="${HOME}/globus-toolkit"

cd "${HOME}"
wget "http://www.globus.org/ftppub/latest-stable/gt-latest-stable-all-source-installer.tar.gz"
tar -vxzf gt-latest-stable-all-source-installer.tar.gz
cd gt*-all-source-installer
GT_INSTALLER_DIR="$(pwd)"
./configure --prefix="${INSTALL_DIR}"
make gridftp install

cd "${HOME}"
rm -rf "${GT_INSTALLER_DIR}"
rm -f "gt-latest-stable-all-source-installer.tar.gz"

cat >> "${HOME}/.bashrc" <<EOF

export GLOBUS_LOCATION="${INSTALL_DIR}"
. \${GLOBUS_LOCATION}/etc/globus-user-env.sh

EOF

export GLOBUS_LOCATION="${INSTALL_DIR}"
. "${GLOBUS_LOCATION}/etc/globus-user-env.sh"
