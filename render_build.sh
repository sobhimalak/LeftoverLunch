#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies from root
pip install -r requirements.txt
pip install django-unfold

cd leftoverlunch

python manage.py collectstatic --no-input
python manage.py migrate
