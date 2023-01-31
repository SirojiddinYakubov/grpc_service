#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $POSTGRES_HOST $DATABASE_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

pip install -r requirements.txt
echo "Successfully installed requirements.txt"

alembic upgrade head

# Start server
echo "Starting server"
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload



