from django.db import models
   
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
    collect_day = models.CharField(max_length=50, choices=DAY_CHOICES, default=TODAY)
    collect_time_start = models.CharField(max_length=5, choices=TIME_CHOICES, default='11:00')
    collect_time_end = models.CharField(max_length=5, choices=TIME_CHOICES, default='12:00')
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=200)
    allergy = models.ManyToManyField('Allergie', related_name='items')
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Categorie', related_name='items')
        

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
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Categorie(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

    

class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField(
        'MenuItem', related_name='order', blank=True)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
    
