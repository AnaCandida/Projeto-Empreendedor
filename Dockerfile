FROM python:3.10-alpine3.13
LABEL maintainer="Grupo TCC: Ana Quadros, Emerson Felippini, Hellen de Freitas, Lauro Neto, Matheus dos Santos, Sinara Mathias"

ENV PYTHONUNBUFFERED 1
ENV PATH="/py/bin:$PATH"
RUN apk update && apk add postgresql-client postgresql-dev

COPY ./requirements.txt /requirements.txt
COPY ./requirements.dev.txt /requirements.dev.txt
COPY ./bora_la /bora_la
COPY  ./start-dev.sh /bora_la/start-dev.sh
RUN chmod +x /bora_la/start-dev.sh
COPY pyproject.toml .flake8 /bora_la/

WORKDIR /bora_la
EXPOSE 8000

ARG DEV= False
RUN pip install --upgrade pip
RUN apk add --no-cache postgresql-dev build-base
RUN pip install -r /requirements.txt
RUN pip install -r /requirements.dev.txt
