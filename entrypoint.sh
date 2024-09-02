#!/bin/sh

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
while ! nc -z $DJANGO_DATABASE_HOST $DJANGO_DATABASE_PORT; do
  sleep 1
done

echo "Database is ready. Starting the application..."
exec "$@"