FROM node:18-alpine AS web

RUN npm i -g pnpm

WORKDIR /workspace

COPY . .

RUN pnpm install

RUN pnpm build:prod

# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster as server

# Port used by this container to serve HTTP.
EXPOSE 8000

ENV PYTHONUNBUFFERED=1

ENV PORT=8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    gdal-bin \
    libgdal-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /

RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Copy the source code of the project into the container.
COPY . .

COPY --from=web /workspace/dist /app/dist

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

LABEL org.opencontainers.image.source https://github.com/zisake/geo-ldn

ENV ENV=production

ENV NODE_ENV=production

CMD set -xe; python manage.py migrate --noinput; gunicorn --bind=0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=app.settings app.wsgi:application
