#!/bin/sh
set -e

# Run database migrations (waits until DB is available if necessary)
python manage.py migrate --noinput

# Then exec the main container command
exec "$@"
