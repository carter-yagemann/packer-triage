#!/bin/bash
set -e

if [ ! -f 'config/frontend.conf' ]; then
    echo "Cannot find config/frontend.conf, make sure:"
    echo "    1) You're in the project's root directory"
    echo "    2) You've configured the project"
    exit 1
fi

source 'config/frontend.conf'
source 'config/database.conf'

docker build -t packer-triage-frontend frontend

if [ "$FRONTEND_HOST_BIND" == 'local' ]; then
    NETWORK_OPTS="--net=packertriage --name=frontend -p 127.0.0.1:9000:9000"
else
    NETWORK_OPTS="-p \"${FRONTEND_HOST_BIND}:9000\""
fi

docker run -it --rm                                \
    -e "MONGO_ADDRESS=${DB_MONGO_ADDRESS}"         \
    -e "MONGO_PASS=${DB_MONGO_PASSWORD}"           \
    -v "${FRONTEND_HOST_LOG_DIR}:/logs"            \
    $NETWORK_OPTS                                  \
    packer-triage-frontend                         \
        --error-logfile /logs/frontend-error.log   \
        --access-logfile /logs/frontend-access.log \
        --bind 0.0.0.0:9000                        \
        -w "$FRONTEND_NUM_WORKERS"                 \
        api:app
