from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import *
from django.http import Http404
import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import DetailView
from django.db.models import Q





class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class single_page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/single_page.html')
    
class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/register.html')


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items,
            'search_query': query
        }

        return render(request, 'customer/menu.html', context)


    
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
        order = OrderModel.objects.create(
            price=price,
            is_paid=False)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price,
        }
        return redirect('order_confirmation', pk=order.pk)




class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        if pk is not None:
            # Handle the case when a valid primary key is provided
            order = OrderModel.objects.get(pk=pk)
            context = {
                'pk': order.pk,
                'items': order.items,
                'price': order.price,
                'order': order,
                'isPaid': order.is_paid,
            }
        else:
            # Handle the case when no primary key is provided (for empty cart, etc.)
            context = {
                'pk': None,
                'items': [],
                'price': 0,
                'order': None,
                'isPaid': False,
            }
            
        return render(request, 'customer/order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        print("Received POST request in OrderConfirmation view.")
        print(request.body)
        data = json.loads(request.body)
        
        if data['isPaid']:
            print("Payment received. Marking the order as paid.")
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()
            print("Order status updated:", order.is_paid)
        else:
            print("Payment not received.")
        return redirect('order_pay_confirmation')

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


