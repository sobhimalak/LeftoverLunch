

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from customer.views import *
from customer import views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('order/', Order.as_view(), name='order'),
    path('single_page/', single_page.as_view(), name='single_page'),
    path('order_confirmation/<int:pk>/', views.OrderConfirmation.as_view(), name='order_confirmation'),

    
    path('payment-confirmation/', OrderPayConfirmation.as_view(), name='payment-confirmation'),
    path('register/', Register.as_view(), name='register'),
    path('cart/', views.Order.as_view(), name='cart'),
    path('order_confirmation/', OrderConfirmation.as_view(), name='order_confirmation'),


]   

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
