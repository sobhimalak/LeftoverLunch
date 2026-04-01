import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leftoverlunch.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = "admin"
password = "leftoversadmin!"
email = "admin@leftoverlunch.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser created successfully: {username}")
else:
    u = User.objects.get(username=username)
    u.set_password(password)
    u.save()
    print(f"Superuser {username} password updated successfully")
