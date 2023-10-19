from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Categorie)
admin.site.register(OrderModel)
admin.site.register(Allergie)


admin.site.site_header = 'Leftover Lunch Admin'
admin.site.site_title = 'Custom Admin Title'