# VueJS build
FROM node:lts-alpine AS build-assets

WORKDIR /app
ARG VITE_API_URL=/api
ARG VITE_BLOG_LINK=https://medium.com/@metamixblog
COPY ./frontend/package.json ./frontend/package-lock.json /app/frontend/
RUN cd /app/frontend && npm install -g npm@9.5.0 && npm install
COPY ./frontend /app/frontend
RUN cd /app/frontend && npm run build

# Django build
FROM python:3.8-bullseye

ENV PYTHONUNBUFFERED 1
ARG DEV_BUILD
WORKDIR /app

RUN apt update \
  && apt upgrade -y \
  && apt install -y build-essential ffmpeg gettext gnupg make python3-dev wget \
  && echo "deb http://apt.postgresql.org/pub/repos/apt bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
  && wget --quiet -O /etc/apt/trusted.gpg.d/postgres.asc https://www.postgresql.org/media/keys/ACCC4CF8.asc \
  && apt update \
  && apt install -y postgresql-client-14 libpq-dev \
  && apt upgrade -y \
  && apt purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt clean \
  && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -U pip

COPY requirements.txt /app/
COPY requirements-development.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt \
  && if [ "$(echo $DEV_BUILD | tr a-z A-Z)" = "TRUE" ]; then pip install --no-cache-dir -r /app/requirements-development.txt; fi

COPY . /app/

COPY --from=build-assets /app/frontend/build/index.html /app/metamemoapp/templates/
COPY --from=build-assets /app/frontend/build/favicon.svg /app/metamemoapp/templates/
COPY --from=build-assets /app/frontend/build/static/* /app/metamemoapp/static/

CMD "/app/bin/web.sh"
