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

# Check static files structure
echo "Static files structure:"
ls -la staticfiles/images/ || echo "No images directory found"
ls -la staticfiles/css/ || echo "No css directory found"
ls -la staticfiles/js/ || echo "No js directory found"

# Run migrations
python manage.py migrate --no-input 