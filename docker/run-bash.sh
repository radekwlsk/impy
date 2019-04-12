#!/usr/bin/env bash

export DOCKER_PATH=$(dirname $(readlink -e $0))

. ${DOCKER_PATH}/common.sh

exec docker-compose -f ${COMPOSE_YAML} run --rm ${DOCKER_CONTAINER} /bin/bash --rcfile ""
