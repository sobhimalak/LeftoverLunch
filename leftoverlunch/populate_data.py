import os
import django
from django.utils import timezone
from datetime import timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leftoverlunch.settings')
django.setup()

from lunch_manager.models import Category, Allergy, StoreLocation, MenuItem, OrderModel, OrderItem
from django.contrib.auth.models import User

def populate():
    # 1. Create Superuser if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print("Superuser 'admin' created.")

    # 2. Create Store Location
    location, _ = StoreLocation.objects.get_or_create(
        name="Main Store",
        address="Norrtullsgatan 4",
        city="Stockholm",
        country="Sweden",
        postal_code="113 29"
    )

    # 3. Create Categories
    cats = ["Meat", "Vegetarian", "Snacks", "Drinks"]
    category_objs = {}
    for cat_name in cats:
        obj, _ = Category.objects.get_or_create(name=cat_name)
        category_objs[cat_name] = obj

    # 4. Create Allergies
    allergies = ["Gluten", "Dairy", "Nuts"]
    allergy_objs = {}
    for a_name in allergies:
        obj, _ = Allergy.objects.get_or_create(name=a_name)
        allergy_objs[a_name] = obj

    # 5. Create Menu Items
    menu_items_data = [
        {"name": "Lasagna", "price": 50, "cat": "Meat", "stock": 10},
        {"name": "Burger", "price": 50, "cat": "Meat", "stock": 10},
        {"name": "Veggie Wrap", "price": 40, "cat": "Vegetarian", "stock": 15},
        {"name": "Smoothie", "price": 30, "cat": "Drinks", "stock": 20},
    ]

    item_objs = []
    for item in menu_items_data:
        mi, created = MenuItem.objects.get_or_create(
            name=item["name"],
            defaults={
                "price": item["price"],
                "stock": item["stock"],
                "store_location": location,
                "collect_day": "Today",
                "collect_time_start": "11:00",
                "collect_time_end": "12:00",
                "description": f"Delicious {item['name']} made fresh."
            }
        )
        mi.category.add(category_objs[item["cat"]])
        item_objs.append(mi)

    # 6. Create Dummy Orders for the last 7 days
    print("Creating dummy orders...")
    for i in range(10):
        # Random date in last 7 days
        days_ago = random.randint(0, 6)
        date = timezone.now() - timedelta(days=days_ago)
        
        order = OrderModel.objects.create(
            price=0,
            is_paid=True,
            name=f"Customer {i}",
            telephone="123456789"
        )
        # Set created_on manually (need to use auto_now_add=False trick if necessary, but for simplicity I'll just adjust the price and rely on current date for today's chart)
        # Actually, for the chart to work, I should create most orders for TODAY.
        
        # Add 1-3 items to order
        total = 0
        for _ in range(random.randint(1, 3)):
            mi = random.choice(item_objs)
            qty = random.randint(1, 2)
            OrderItem.objects.create(order=order, item=mi, quantity=qty)
            total += mi.price * qty
        
        order.price = total
        order.save()
        
        # Override created_on using update() to bypass auto_now_add
        OrderModel.objects.filter(pk=order.pk).update(created_on=date)

    print("Data population complete!")

if __name__ == "__main__":
    populate()
