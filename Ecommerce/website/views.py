from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime

# Create your views here.


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'website/index.html', context)


def about(request):
    context = {}
    return render(request, 'website/about.html', context)


def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'website/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)



from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        data = json.loads(request.body)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            full_name=data['form']['name'],
            mobile_num=data['form']['phone_num'],
        )

    else:
        print('User is not logged in...')
    return JsonResponse('Payment Complete', safe=False)


def payment(request):
    context = {}
    return render(request, 'website/payment.html', context)


def contact(request):
    context = {}
    return render(request, 'website/contact.html', context)


def service(request):
    context = {}
    return render(request, 'website/service.html', context)


def shop(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'website/shop.html', context)


def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'website/product.html', context)


def single(request):
    context = {}
    return render(request, 'website/single.html', context)
