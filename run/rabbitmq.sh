#!/bin/bash
set -e

if [ ! -f 'config/database.conf' ]; then
    echo "Cannot find config/database.conf, make sure:"
    echo "    1) You're in the project's root directory"
    echo "    2) You've configured the project"
    exit 1
fi

source 'config/database.conf'

if [ "$DB_RABBIT_PASSWORD" == "another_secret" ]; then
    echo "You must change DB_RABBIT_PASSWORD in config/database.conf!"
    exit 2
fi

# Make sure RabbitMQ has permission to write log to host
HOST_RABBIT_LOGFILE="${DB_HOST_LOG_DIR}/rabbit.log"
if [ ! -f "$HOST_RABBIT_LOGFILE" ]; then
    touch "$HOST_RABBIT_LOGFILE"
    chmod o+w "$HOST_RABBIT_LOGFILE"
fi

if [ "$DB_RABBIT_ADDRESS" == "local" ]; then
    NETWORK_OPTS="--ip=10.0.22.3 -p 127.0.0.1:9002:5672"
else
    NETWORK_OPTS="-p \"${DB_RABBIT_ADDRESS}:5672\""
fi

docker run -it --rm                                  \
    -e "RABBITMQ_DEFAULT_USER=rabbit"                \
    -e "RABBITMQ_DEFAULT_PASS=${DB_RABBIT_PASSWORD}" \
    -e "RABBITMQ_NODE_PORT=5672"                     \
    -e "RABBITMQ_LOGS=/logs/rabbit.log"              \
    -v "${DB_HOST_LOG_DIR}:/logs"                    \
    $NETWORK_OPTS                                    \
    rabbitmq:3
