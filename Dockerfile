FROM python:3.11-slim-bullseye

ARG API_PORT=API_PORT

WORKDIR /servive

COPY pyproject.toml poetry.lock README.md ./
COPY scripts/ /servive/scripts/
COPY src/ /servive/src/

RUN pip install poetry==1.8.3 && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    chmod +x scripts/api.sh
