

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customer.views import *
from customer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('order/', Order.as_view(), name='order'),
    path('single-page/', SinglePage.as_view(), name='single-page'),
    path('order-confirmation/<int:pk>', OrderConfirmation.as_view(),name='order-confirmation'),
    path('payment-confirmation/<int:pk>', OrderPayConfirmation.as_view(),name='payment-confirmation'),
    path('register/', Register.as_view(), name='register'),
    


]   

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
