from django.shortcuts import render
from django.views import View
from .models import MenuItem, Category, OrderModel
from django.http import Http404


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class single_page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/single_page.html')

class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/login.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre', stock__gt=0)
        desserts = MenuItem.objects.filter(category__name__contains='Dessert', stock__gt=0)
        drinks = MenuItem.objects.filter(category__name__contains='Drink', stock__gt=0)
        
        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item_id in items:
            try:
                menu_item = MenuItem.objects.get(pk=int(item_id), stock__gt=0)
                item_data = {
                    'id': menu_item.pk,
                    'name': menu_item.name,
                    'price': menu_item.price
                }

                order_items['items'].append(item_data)

                # Deduct 1 from the available stock after adding to the order
                menu_item.stock -= 1
                menu_item.save()

            except MenuItem.DoesNotExist:
                # Handle the case where the item does not exist or is out of stock
                raise Http404("Item not found or out of stock")

        # Calculate total price and item IDs outside the loop
        price = sum(item['price'] for item in order_items['items'])
        item_ids = [item['id'] for item in order_items['items']]

        # Create an order and add items to it
        order = OrderModel.objects.create(price=price)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)
