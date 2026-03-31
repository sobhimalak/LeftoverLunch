from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *

# create a MenuItem admin to view the menu item in the admin page
class MenuItemAdmin(ModelAdmin): 
    list_display = ('name', 'collect_day', 'collect_time_start', 'collect_time_end', 'stock', 'price')
    search_fields = ('name', 'collect_day', 'collect_time_start', 'collect_time_end', 'stock', 'price')
    ordering = ('collect_day', 'collect_time_start', 'collect_time_end', 'stock', 'price')

# create a OrderModel admin to view the order in the admin page
class OrderModelAdmin(ModelAdmin):
    list_display = ('id','created_on', 'price','is_paid')
    search_fields = ('id','created_on', 'price','is_paid')
    ordering = ('id','created_on', 'price','is_paid')

# Register your models here.
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Category, ModelAdmin)
admin.site.register(OrderModel, OrderModelAdmin)
admin.site.register(Allergy, ModelAdmin)
admin.site.register(StoreLocation, ModelAdmin)