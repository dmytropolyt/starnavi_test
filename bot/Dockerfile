FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ../bot /bot
COPY ./requirements.txt /tmp/requirements.txt

WORKDIR /bot

RUN apk update \
    && apk add --no-cache curl \
    && rm -rf /var/cache/apk/*


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r  /tmp/requirements.txt && \
    rm -rf /tmp

ENV PATH="/scripts:/py/bin:$PATH"