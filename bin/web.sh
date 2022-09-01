#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

if [ -z ${PORT+x} ]; then
	PORT=5000
fi
HOST_PORT="0.0.0.0:$PORT"

if [[ $(echo $DEV_BUILD | tr a-z A-Z) = "TRUE" ]]; then
	python manage.py runserver $HOST_PORT
else
	if [ -z ${WEB_WORKERS+x} ]; then
		WEB_WORKERS=4
	fi

	OPTS="--bind=$HOST_PORT --chdir=/app --log-file - --workers=$WEB_WORKERS"
	if [[ $(echo $USE_ASGI | tr a-z A-Z) = "TRUE" ]]; then
		APP_MODULE="metamemo.asgi:application"
		OPTS="$OPTS --worker-class uvicorn.workers.UvicornWorker"
	else
		APP_MODULE="metamemo.wsgi:application"
	fi
	gunicorn $OPTS $APP_MODULE
fi
