FROM python:3.8-slim-bullseye

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

CMD "/app/bin/web.sh"
