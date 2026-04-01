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

python manage.py collectstatic --no-input
echo "--- STATICFILES CONTENT ---"
ls -R staticfiles/
python manage.py migrate
python create_admin.py

echo "Build finished at $(date)"
