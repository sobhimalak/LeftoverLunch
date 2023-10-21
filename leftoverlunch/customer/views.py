from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import *
from django.http import Http404
from django.views.generic import DetailView



class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class item_detail(View):
    def get(self, request, pk, *args, **kwargs):
        return render(request, 'customer/item_detail.html')
    
class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/register.html')

class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/login.html')
    

    
class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        all_items = MenuItem.objects.all()
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre', stock__gt=0)
        desserts = MenuItem.objects.filter(category__name__contains='Dessert', stock__gt=0)
        drinks = MenuItem.objects.filter(category__name__contains='Drink', stock__gt=0)
        
        store_location = StoreLocation.objects.first()

        # pass into context
        context = {
            'all_items': all_items,
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
            'store_location': store_location, 
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
                    'price': menu_item.price,

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
    

class ItemDetailView(DetailView):
    model = MenuItem
    template_name = 'customer/item_detail.html'
    context_object_name = 'item'
    app_name = 'customer'