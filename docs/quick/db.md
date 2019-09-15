# Databases

This project uses two databases: MongoDB and RabbitMQ. The former is for storing
data and the latter passes messages between the frontend and the workers.

The `run` directory contains scripts for starting each database as a docker container.

## Starting a MongoDB instance

Simply run the script: `./run/mongo.sh`
