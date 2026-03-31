from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from lunch_manager.models import OrderModel, MenuItem

def dashboard_callback(request, context):
    print("DEBUG: Dashboard callback called!")
    # Total Revenue
    total_revenue = OrderModel.objects.filter(is_paid=True).aggregate(Sum('price'))['price__sum'] or 0
    
    # Total Orders
    total_orders = OrderModel.objects.count()
    
    # Total Menu Items
    total_menu_items = MenuItem.objects.count()
    
    # Chart: Revenue by Day (Last 7 Days)
    today = timezone.now().date()
    revenue_labels = []
    revenue_values = []
    
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        revenue_labels.append(day.strftime("%a"))
        daily_revenue = OrderModel.objects.filter(
            created_on__date=day, 
            is_paid=True
        ).aggregate(Sum('price'))['price__sum'] or 0
        revenue_values.append(float(daily_revenue))
        
    # Chart: Order Status (Paid vs Unpaid)
    paid_count = OrderModel.objects.filter(is_paid=True).count()
    unpaid_count = OrderModel.objects.filter(is_paid=False).count()
    
    # Stats Cards Data
    custom_kpi_stats = [
        {
            "title": "Total Revenue",
            "value": f"{total_revenue:,.2f} kr",
            "description": "Gross revenue from paid orders",
            "icon": "payments",
        },
        {
            "title": "Total Orders",
            "value": str(total_orders),
            "description": "Total number of orders placed",
            "icon": "shopping_cart",
        },
        {
            "title": "Menu Items",
            "value": str(total_menu_items),
            "description": "Active items in the menu",
            "icon": "restaurant_menu",
        },
    ]

    context.update({
        "custom_kpi_stats": custom_kpi_stats,
        "revenue_chart": {
            "labels": revenue_labels,
            "datasets": [{
                "label": "Revenue (kr)",
                "data": revenue_values,
                "backgroundColor": "#6366f1",
                "borderColor": "#6366f1",
            }]
        },
        "order_status_chart": {
            "labels": ["Paid", "Unpaid"],
            "datasets": [{
                "label": "Orders",
                "data": [paid_count, unpaid_count],
                "backgroundColor": ["#10b981", "#ef4444"],
            }]
        }
    })
    return context
