FROM python:3.13-slim-bookworm

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends \
    libcairo2 \
    pango1.0-tools \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi8 \
    libxml2 \
    libxslt1.1 \
    libjpeg62-turbo \
    fonts-liberation \
    fonts-dejavu-core \
    shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ARG APP_VERSION="0.0.0"
ENV SETUPTOOLS_SCM_PRETEND_VERSION=${APP_VERSION}
WORKDIR /app

COPY pyproject.toml ./
COPY api ./api
COPY pdf ./pdf
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -e .

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN git clone --depth=1 --filter=blob:none --sparse \
        https://github.com/joaodalcastanher/divinum-officium.git /tmp/divoff \
    && cd /tmp/divoff \
    && git sparse-checkout set \
        web/www/missa/Latin \
        web/www/missa/English \
        web/www/missa/Polski \
        web/www/missa/Portugues \
        web/www/horas/Latin/Commune \
        web/www/horas/English/Commune \
        web/www/horas/Polski/Commune \
    && mkdir -p resources/divinum-officium/web/www \
    && cp -r /tmp/divoff/web/www/missa resources/divinum-officium/web/www/missa \
    && cp -r /tmp/divoff/web/www/horas resources/divinum-officium/web/www/horas \
    && rm -rf /tmp/divoff

COPY resources/ordo ./resources/ordo
COPY resources/propers ./resources/propers
COPY resources/supplement ./resources/supplement
COPY resources/divinum-officium-local ./resources/divinum-officium-local

ENV PORT=8080
CMD gunicorn --bind "0.0.0.0:${PORT}" -w 2 -k uvicorn.workers.UvicornWorker api.app:app --access-logfile -
