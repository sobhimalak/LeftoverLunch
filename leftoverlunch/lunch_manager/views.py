from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from .models import *
from django.http import Http404
import json
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse




class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'lunch_manager/index.html')

class SinglePage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'lunch_manager/single_page.html')
    
class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'lunch_manager/register.html')



class Order(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")

        # get every item from each category and apply search filter if query is present
        all_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        ) if query else MenuItem.objects.all()
        
        print("SQL Query:", all_items.query)

        # get every category for the filter bar
        categories = Category.objects.all()
        store_location = StoreLocation.objects.first()

        # get current cart count
        cart_count = 0
        order_id = request.session.get('active_order_id')
        if order_id:
            try:
                order = OrderModel.objects.get(pk=order_id, is_paid=False)
                cart_count = sum(oi.quantity for oi in order.order_items.all())
            except OrderModel.DoesNotExist:
                pass

        # pass into context
        context = {
            'all_items': all_items,
            'categories': categories,
            'store_location': store_location, 
            'cart_count': cart_count,
        }

        # render the template
        return render(request, 'lunch_manager/order.html', context)

    def post(self, request, *args, **kwargs):
        items = request.POST.getlist('items[]')
        
        if not items:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'No items selected'})
            return redirect('order')

        # Check for existing order in session
        order_id = request.session.get('active_order_id')
        if order_id:
            try:
                order = OrderModel.objects.get(pk=order_id, is_paid=False)
            except OrderModel.DoesNotExist:
                order = OrderModel.objects.create(price=0, is_paid=False)
                request.session['active_order_id'] = order.pk
        else:
            order = OrderModel.objects.create(price=0, is_paid=False)
            request.session['active_order_id'] = order.pk
        
        total_price = order.price
        from collections import Counter
        item_counts = Counter(items)

        for item_id, count in item_counts.items():
            try:
                menu_item = MenuItem.objects.get(pk=int(item_id))
                if menu_item.stock >= count:
                    menu_item.stock -= count
                    menu_item.save()
                    
                    # Check if item already exists in this order
                    order_item, created = OrderItem.objects.get_or_create(
                        order=order,
                        item=menu_item,
                        defaults={'quantity': 0}
                    )
                    order_item.quantity += count
                    order_item.save()
                    
                    total_price += menu_item.price * count
                else:
                    available = menu_item.stock
                    if available > 0:
                        menu_item.stock = 0
                        menu_item.save()
                        
                        order_item, created = OrderItem.objects.get_or_create(
                            order=order,
                            item=menu_item,
                            defaults={'quantity': 0}
                        )
                        order_item.quantity += available
                        order_item.save()
                        
                        total_price += menu_item.price * available
            except MenuItem.DoesNotExist:
                continue

        order.price = total_price
        order.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Count total items in the order for the navbar badge
            cart_count = sum(oi.quantity for oi in order.order_items.all())
            return JsonResponse({
                'success': True, 
                'cart_count': cart_count,
                'total_price': float(total_price),
                'message': 'Added to cart!'
            })

        return redirect('order-confirmation', pk=order.pk)

class UpdateOrderItemQuantity(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        order_item_id = data.get('order_item_id')
        action = data.get('action') # 'plus' or 'minus'
        
        order_item = get_object_or_404(OrderItem, pk=order_item_id)
        menu_item = order_item.item
        
        if action == 'plus':
            if menu_item.stock > 0:
                menu_item.stock -= 1
                order_item.quantity += 1
                menu_item.save()
                order_item.save()
        elif action == 'minus':
            if order_item.quantity > 0:
                menu_item.stock += 1
                order_item.quantity -= 1
                menu_item.save()
                if order_item.quantity == 0:
                    order_item.delete()
                else:
                    order_item.save()
        
        # Recalculate order total
        order = order_item.order
        new_total = sum(oi.total_price for oi in order.order_items.all())
        order.price = new_total
        order.save()
        
        return JsonResponse({
            'success': True,
            'new_quantity': order_item.quantity if order_item.pk else 0,
            'new_item_total': float(order_item.total_price) if order_item.pk else 0,
            'new_order_total': float(new_total)
        })




class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        # If pk is 0, try to get from session
        if pk == 0:
            pk = request.session.get('active_order_id')
            
        if pk:
            try:
                order = OrderModel.objects.get(pk=pk)
                # If order is already paid, it shouldn't be in the active cart view
                if order.is_paid:
                    return redirect('order')
                    
                context = {
                    'pk': order.pk,
                    'items': order.order_items.all(),
                    'price': order.price,
                    'order': order,
                    'isPaid': order.is_paid,
                }
            except OrderModel.DoesNotExist:
                return redirect('order')
        else:
            # No pk and no session order
            return redirect('order')
            
        return render(request, 'lunch_manager/order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)
        
        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()
           
        return redirect('payment-confirmation', pk=pk)

class OrderPayConfirmation(View):
    def get(self, request, pk,*args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'pk': pk,
            'isPaid': order.is_paid,
            'order': order,
        }
        return render(request, 'lunch_manager/order_pay_confirmation.html',context)


