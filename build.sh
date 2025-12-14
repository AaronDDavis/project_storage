#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Convert static files for production
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Create Superuser automatically
python scripts/create_superuser.py
