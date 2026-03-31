#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies from root
pip install -r requirements.txt
pip install django-unfold

cd leftoverlunch

# Redirect all output to a log file
LOG_FILE="static/build_log.txt"
echo "Build started at $(date)" > $LOG_FILE

python manage.py collectstatic --no-input >> $LOG_FILE 2>&1
python manage.py migrate >> $LOG_FILE 2>&1

echo "Build finished at $(date)" >> $LOG_FILE
