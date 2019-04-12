#!/usr/bin/env bash

export DOCKER_PATH=$(dirname $(readlink -e $0))

. ${DOCKER_PATH}/common.sh

case ${DOCKER_CONTAINER} in
    django_api)
        DJANGO_PORT=8000
        ;;
    django_receiver)
        DJANGO_PORT=8001
        ;;
    *)
        echo "Unknown DOCKER_CONTAINER: \"${DOCKER_CONTAINER}\""
        exit 1
esac

exec docker-compose -f ${COMPOSE_YAML} run --rm --service-ports ${DOCKER_CONTAINER} \
    python3 manage.py runserver 0.0.0.0:${DJANGO_PORT}
