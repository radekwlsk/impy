#!/usr/bin/env bash

export DOCKER_PATH="$(cd "$(dirname "$0")" && pwd -P)"
#export DOCKER_ENV=test

. ${DOCKER_PATH}/common.sh

docker-compose -f ${COMPOSE_YAML} run --rm ${DOCKER_CONTAINER} \
    python3 manage.py migrate --no-input
docker-compose -f ${COMPOSE_YAML} run --rm ${DOCKER_CONTAINER} \
    python3 manage.py test -- $*
