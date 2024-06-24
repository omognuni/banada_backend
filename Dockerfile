FROM python:3.12-alpine3.20

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user && \
    mkdir -p /app/media && \
    mkdir -p /app/static && \
    chown -R django-user:django-user /app/media && \
    chown -R django-user:django-user /app/static && \
    chmod -R 755 /app/media && \
    chmod -R 755 /app/static

ENV PATH="/py/bin:$PATH"
RUN python manage.py collectstatic

USER django-user
