#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Creating staticfiles_build directory..."
mkdir -p staticfiles_build/static

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Static files ready at: staticfiles_build/static"
ls -la staticfiles_build/static/ 2>/dev/null || echo "Directory contents not accessible"
