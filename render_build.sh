#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies from root
pip install -r requirements.txt
pip install django-unfold

# Smart CD: check if we are in the root and need to go into the project folder
if [ -d "leftoverlunch" ] && [ -f "leftoverlunch/manage.py" ]; then
    echo "Transitioning to project subdirectory 'leftoverlunch'..."
    cd leftoverlunch
fi

# Ensure staticfiles exists
mkdir -p staticfiles
LOG_FILE="staticfiles/build_log.txt"
echo "Build started at $(date)" > $LOG_FILE

python manage.py collectstatic --no-input >> $LOG_FILE 2>&1
echo "--- STATICFILES CONTENT ---" >> $LOG_FILE
ls -R staticfiles/ >> $LOG_FILE 2>&1
python manage.py migrate >> $LOG_FILE 2>&1
python create_admin.py >> $LOG_FILE 2>&1

echo "Build finished at $(date)" >> $LOG_FILE
