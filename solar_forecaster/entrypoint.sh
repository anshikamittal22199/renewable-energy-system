#!/bin/sh
set -e

# Ensure migrations exist and apply them. `makemigrations` will create migration files
# inside the mounted source directory so they persist on the host during development.
python manage.py makemigrations forecast || true
python manage.py migrate --noinput

# Then exec the main container command
exec "$@"
