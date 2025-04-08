#!/bin/bash
set -e

if [ ! -d "/app/app/migrations" ]; then
    echo "---> Initializing migrations"
    flask db init --directory /app/app/migrations
fi

echo "---> Generating migrations"
flask db migrate --directory /app/app/migrations -m "Initial migration"

echo "---> Applying migrations"
flask db upgrade --directory /app/app/migrations

echo "---> Starting Gunicorn"
exec gunicorn --bind 0.0.0.0:5000 "app:create_app()"