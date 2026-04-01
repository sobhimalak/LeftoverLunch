import os
import django
from django.conf import settings
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leftoverlunch.settings')
django.setup()

def create_user(username, password):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email='', password=password)
        print(f"User {username} created")
    else:
        u = User.objects.get(username=username)
        u.set_password(password)
        u.is_staff = True
        u.is_superuser = True
        u.is_active = True
        u.save()
        print(f"User {username} updated and activated")

print(f"Connecting to database: {connection.settings_dict.get('HOST', 'unknown')}")
create_user('admin', 'leftoversadmin!')
create_user('sobhi_admin', 'leftoversadmin!')
