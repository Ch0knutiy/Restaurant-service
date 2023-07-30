FROM python:3.10-slim

ARG BUILD_DEPS="curl"
RUN apt-get update && apt-get install -y $BUILD_DEPS \
    && apt-get -y install libpq-dev gcc

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.5.1 POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /y_lab
COPY . .

EXPOSE 8000

RUN poetry config virtualenvs.create false
RUN poetry install --no-root