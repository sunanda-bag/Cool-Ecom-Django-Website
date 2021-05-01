from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name= 'about'),
    path('checkout/', views.checkout, name= 'checkout'),
    path('payment/', views.payment, name= 'payment'),
    path('contact/', views.contact, name= 'contact'),
    path('service/', views.service, name= 'service'),
    path('shop/', views.shop, name= 'shop'),
    path('product/', views.product, name= 'product'),
    path('single/', views.single, name= 'single'),

    path('update_item/', views.updateItem, name= 'update_item'),
    path('process_order/', views.processOrder, name= 'process_order'),
]
