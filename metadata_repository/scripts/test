#!/bin/bash

SCRIPTS_DIR=$( cd $(dirname $0); pwd -P )
PROJECT_DIR=$( cd "${SCRIPTS_DIR}/.."; pwd -P )

export CSRF_DISABLED=True
export DATABASE_URL="sqlite://"

cd "$PROJECT_DIR"
nose2 \
    --project-directory . \
    --start-dir tests \
    --log-capture \
    "$@"
