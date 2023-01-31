#!/bin/bash

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."
  while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
    sleep 0.1
  done
  echo "PostgreSQL started"
fi

poetry install
echo "Successfully installed packages"

alembic upgrade head

echo "Starting server"
python app/server.py