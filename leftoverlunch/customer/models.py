from django.db import models
from django.conf import settings


class StoreLocation(models.Model):
    name = models.CharField(max_length=255, help_text='Enter the name of your store')
    address = models.CharField(max_length=255, help_text='Enter the store address')
    city = models.CharField(max_length=100, help_text='Enter the city')
    country = models.CharField(max_length=100, help_text='Enter the country')
    postal_code = models.CharField(max_length=20, help_text='Enter the postal code')
    store_link = models.URLField(max_length=200, help_text='Enter the link to your store location on Google Maps', blank=True)

    def __str__(self):
        return self.name
   
class MenuItem(models.Model):
    TODAY = 'Today'
    TOMORROW = 'Tomorrow'

    DAY_CHOICES = [(TODAY, 'Today'),(TOMORROW, 'Tomorrow'),]
    
    # Generate TIME_CHOICES for a time span between 11:00 AM and 12:00 PM
    TIME_CHOICES = [(f'{hour:02}:{minute:02}', f'{hour % 12 or 12}:{minute:02} {"AM" if hour < 12 else "PM"}')
                    for hour in range(11, 24)  # Hours from 11 to 23 (24-hour format)
                    for minute in range(0, 60, 15)]  # Minutes with a step of 15 minutes (0, 15, 30, 45)
    def is_out_of_stock(self):
        return self.stock == 0
    
   
    name = models.CharField(max_length=100)
    store_location = models.ForeignKey(StoreLocation, on_delete=models.CASCADE, related_name='menu_items', null=True, blank=True, help_text='Select the store location for this item')
    collect_day = models.CharField(max_length=50, choices=DAY_CHOICES, default=TODAY, help_text='Select the day to collect order')
    collect_time_start = models.CharField(max_length=5, choices=TIME_CHOICES, default='11:00', help_text='Select the time to collect order')
    collect_time_end = models.CharField(max_length=5, choices=TIME_CHOICES, default='12:00')
    stock = models.PositiveIntegerField(default=0, help_text='Enter the number of items in stock')
    description = models.TextField(max_length=200, help_text='Enter a brief description of the item (Max. 200 characters)')
    allergy = models.ManyToManyField('Allergie', related_name='items', help_text='Select the allergies for this item (if any, Max. 5)')
    image = models.ImageField(upload_to='menu_images/',help_text='Upload an image of the item (640X427)')
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text='Enter the price of the item (Max. 50.00)')
    category = models.ManyToManyField('Categorie', related_name='items', help_text='Select the categories for this item')


    def __str__(self):
        return self.name
    # this is a property decorator that will return the url of the image
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



class Allergie(models.Model):
    name = models.CharField(max_length=50, help_text='Enter the name of the allergy')
    def __str__(self):
        return self.name
    
class Categorie(models.Model):
    name = models.CharField(max_length=50, help_text='Enter the name of the category(e.g. Appetizer, Entre, Dessert, Drink)')
    def __str__(self):
        return self.name

    

class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField(
        'MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    telephone = models.CharField(max_length=50, blank=True)
    is_paid = models.BooleanField(default=False, help_text='Check this box if the order has been paid for')

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
    
