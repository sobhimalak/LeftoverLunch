from django.contrib import admin
from .models import *


class MenuItemAdmin(admin.ModelAdmin): 
    list_display = ('name', 'collect_day', 'collect_time_start', 'collect_time_end', 'stock', 'price')
    search_fields = ('name', 'collect_day', 'collect_time_start', 'collect_time_end', 'stock', 'price')
    ordering = ('collect_day', 'collect_time_start', 'collect_time_end', 'stock', 'price')

# Register your models here.
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Categorie)
admin.site.register(OrderModel)
admin.site.register(Allergie)
admin.site.register(StoreLocation)

# list display for MenuItem


admin.site.site_header = 'Leftover Lunch Admin'
admin.site.site_title = 'Custom Admin Title'