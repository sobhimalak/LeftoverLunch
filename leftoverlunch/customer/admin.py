from django.contrib import admin
from .models import *

# create a MenuItem admin to view the menu item in the admin page
class MenuItemAdmin(admin.ModelAdmin): 
    list_display = ('name', 'collect_day', 'collect_time_start', 'collect_time_end', 'stock', 'price')
    search_fields = ('name', 'collect_day', 'collect_time_start', 'collect_time_end', 'stock', 'price')
    ordering = ('collect_day', 'collect_time_start', 'collect_time_end', 'stock', 'price')

# create a OrderModel admin to view the order in the admin page
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id','created_on', 'price','is_paid')
    search_fields = ('id','created_on', 'price','is_paid')
    ordering = ('id','created_on', 'price','is_paid')

# Register your models here.
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Categorie)
admin.site.register(OrderModel, OrderModelAdmin)
admin.site.register(Allergie)
admin.site.register(StoreLocation)




admin.site.site_header = 'Leftover Lunch Admin'
admin.site.site_title = 'Custom Admin Title'