#!/bin/bash
set -e

if [ ! -f 'config/database.conf' ]; then
    echo "Cannot find config/database.conf, make sure:"
    echo "    1) You're in the project's root directory"
    echo "    2) You've configured the project"
    exit 1
fi

source 'config/frontend.conf'
source 'config/database.conf'

docker build -t packer-triage-frontend frontend

NETWORK_OPTS="--net=packertriage --name=worker"

if [ "$DB_RABBIT_ADDRESS" == "local" ]; then
    RABBIT_ADDRESS="127.0.0.1:9002"
else
    RABBIT_ADDRESS="${DB_RABBIT_ADDRESS}:5672"
fi


# user must put models in data/models dir
# celery may have logs
docker run -it --rm                                  \
    $NETWORK_OPTS                                    \
    -e "MONGO_ADDRESS=${DB_MONGO_ADDRESS}"           \
    -e "MONG_PASS=${DB_MONGO_PASSWORD}"              \
    -e "RABBITMQ_DEFAULT_USER=rabbit"                \
    -e "RABBITMQ_DEFAULT_PASS=${DB_RABBIT_PASSWORD}" \
    -e "RABBITMQ_ADDRESS=$RABBIT_ADDRESS"            \
    -v "${DB_HOST_DATA_DIR}/models:/models"          \
    -v "${DB_HOST_LOG_DIR}:/logs"                    \
    packer-triage-frontend celery -A worker/tasks worker --loglevel=info

