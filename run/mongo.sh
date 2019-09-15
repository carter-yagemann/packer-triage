#!/bin/bash
set -e

if [ ! -f 'config/database.conf' ]; then
    echo "Cannot find config/database.conf, make sure:"
    echo "    1) You're in the project's root directory"
    echo "    2) You've configured the project"
    exit 1
fi

source 'config/database.conf'

if [ "$DB_MONGO_PASSWORD" == "something_secret" ]; then
    echo "You must change DB_MONGO_PASSWORD in config/database.conf!"
    exit 2
fi

# Make sure MongoDB has permission to write log to host
HOST_MONGO_LOGFILE="${DB_HOST_LOG_DIR}/mongod.log"
if [ ! -f "$HOST_MONGO_LOGFILE" ]; then
    touch "$HOST_MONGO_LOGFILE"
    chmod o+w "$HOST_MONGO_LOGFILE"
fi

# Setup host directory for the database files
HOST_MONGODB_DIR="${DB_HOST_DATA_DIR}/mongo"
if [ ! -d "$HOST_MONGODB_DIR" ]; then
    mkdir "$HOST_MONGODB_DIR"
fi

if [ "$DB_MONGO_ADDRESS" == "local" ]; then
    NETWORK_OPTS="--net=packertriage --name=mongo -p 127.0.0.1:9001:27017"
else
    NETWORK_OPTS="-p \"${DB_MONGO_ADDRESS}:27017\""
fi

docker run -it --rm                                      \
    -e "MONGO_INITDB_ROOT_USERNAME=mongo"                \
    -e "MONGO_INITDB_ROOT_PASSWORD=${DB_MONGO_PASSWORD}" \
    -v "${PWD}/mongo:/conf"                              \
    -v "${DB_HOST_LOG_DIR}:/logs"                        \
    -v "${HOST_MONGODB_DIR}:/data/db"                    \
    $NETWORK_OPTS                                        \
    mongo:bionic                                         \
        --config /conf/mongod.conf
