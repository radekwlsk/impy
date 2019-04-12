#!/usr/bin/env bash

set -ue

export DOCKER_ENV=${DOCKER_ENV:-dev}

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-impy.settings}

export DOCKER_CONTAINER=${DOCKER_CONTAINER:-django_api}

export DOCKER_HOST_NAME=$(hostname)

export COMPOSE_YAML=${DOCKER_PATH}/compose.yaml

docker-compose -f ${COMPOSE_YAML} build

docker-compose -f ${COMPOSE_YAML} run ${DOCKER_CONTAINER} wait-for-postgres.sh postgres_${DOCKER_ENV}
