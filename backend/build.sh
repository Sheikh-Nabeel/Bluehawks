#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Set Django settings module for production
export DJANGO_SETTINGS_MODULE=bluehawks.settings_production

python manage.py collectstatic --no-input
python manage.py migrate 