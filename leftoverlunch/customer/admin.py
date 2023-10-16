from django.contrib import admin
from .models import MenuItem, Category, OrderModel,Allergies

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(Allergies)

admin.site.site_header = 'Leftover Lunch Admin'
admin.site.site_title = 'Custom Admin Title'