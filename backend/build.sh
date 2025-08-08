#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Set Django settings module for production
export DJANGO_SETTINGS_MODULE=bluehawks.settings_production

# Debug: Show static files directories
echo "Static files directories:"
python manage.py collectstatic --no-input --verbosity=2

# Show what was collected
echo "Collected static files:"
ls -la staticfiles/

# Run migrations
python manage.py migrate --no-input 