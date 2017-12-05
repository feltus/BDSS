#!/bin/bash

#
# Running BDSS installed on a remote server via ssh
#
# Note: Change the $HOST and $BDSS variables below according to your server setting
#
# Examples: 
#   1. Show remote BDSS mechanisms
#      ./bdss_remote.sh mechanisms
#
#   2. Copy a file from NCBI to remote /tmp directory
#      ./bdss_remote.sh transfer -u 'ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR039/SRR039885/SRR039885.sra' -d /tmp

HOST=example.com              # Remote host set up with key-based ssh access
BDSS=/usr/local/bin/bdss      # Remote path where BDSS is installed. Change according to your BDSS installation

# Gather arguments
ARGVS=""
for arg in $@; do
  ARGVS="$ARGVS $arg";
done

# Launch BDSS on remote host
echo "Launching BDSS on $HOST"
ssh $HOST "$BDSS $ARGVS"

echo "Done. Return to localhost $HOSTNAME"

