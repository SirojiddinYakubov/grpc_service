FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# Install Poetry
RUN apt clean && apt update && apt install curl netcat vim -y
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY pyproject.toml poetry.lock* /code/

ENV PYTHONPATH=/code
EXPOSE $SVC_PORT

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]