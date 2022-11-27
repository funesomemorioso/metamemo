#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

if [ -z ${PORT+x} ]; then
	PORT=5000
fi
if [ -z ${USE_ASGI+x} ]; then
	USE_ASGI=false
fi
if [ -z ${WEB_WORKERS+x} ]; then
	WEB_WORKERS=4
fi

HOST_PORT="0.0.0.0:$PORT"
OPTS="--bind=$HOST_PORT --chdir=/app --log-file - --workers=$WEB_WORKERS"
if [[ "$(echo $USE_ASGI | tr a-z A-Z)" = "TRUE" ]]; then
	APP_MODULE="metamemo.asgi:application"
	OPTS="$OPTS --worker-class uvicorn.workers.UvicornWorker"
else
	APP_MODULE="metamemo.wsgi:application"
fi
if [[ $(echo $DEV_BUILD | tr a-z A-Z) = "TRUE" ]]; then
	OPTS="$OPTS --reload"
fi

python manage.py collectstatic --no-input
gunicorn $OPTS $APP_MODULE
