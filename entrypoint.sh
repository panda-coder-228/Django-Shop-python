#!/bin/sh

echo "Waiting for Postgresql"
until pg_isready -U "$DB_USER" -d "$DB_NAME" -p"$DB_PORT"; do
    sleep 3
done

echo "Cheking for unapplied migrations"
python manage.py makemigartions --check --dry-run


echo "Applyting migrate"
python manage.py migrate --noinput

echo "Collecting static"
python manage.py collectstatic --noinput

echo "Starting application"
"$@"