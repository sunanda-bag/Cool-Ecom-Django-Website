from django.urls import path
from . import views

app_name = 'website'
urlpatterns = [
    # path('', views.index, name = 'index'),
    path('', views.IndexView.as_view(), name = 'index'),

    path('about/', views.about, name= 'about'),

    # path('checkout/', views.checkout, name= 'checkout'),
    path('checkout/', views.CheckoutView.as_view(), name= 'checkout'),
    path('order-summary/', views.OrderSummaryView.as_view(), name= 'order-summary'),
    
    path('payment/', views.payment, name= 'payment'),
    path('contact/', views.contact, name= 'contact'),
    path('service/', views.service, name= 'service'),

    # path('shop/', views.shop, name= 'shop'),
    path('shop/', views.ShopView.as_view(), name= 'shop'),

    # path('product/', views.product, name= 'product'),
    path('product/', views.ProductsView.as_view(), name= 'product'),

    # path('single/', views.single, name= 'single'),
    path('single/<slug>/', views.ProductDetailView.as_view(), name= 'single'),

    path('add_to_cart/<slug>/', views.add_to_cart, name= 'add_to_cart'),
    path('remove_from_cart/<slug>/', views.remove_from_cart, name= 'remove_from_cart'),
    path('remove_item_from_cart/<slug>/', views.remove_single_item_from_cart, name= 'remove_single_item_from_cart'),

    # path('update_item/', views.updateItem, name= 'update_item'),
    # path('process_order/', views.processOrder, name= 'process_order'),
]
