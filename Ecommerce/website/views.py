from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse, request
import json
import datetime

from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


class IndexView(ListView):
    model = Product
    template_name = 'index.html'


def about(request):
    context = {}
    return render(request, 'about.html', context)


class CheckoutView(ListView):

    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, complete = False)
        context = {'order':order}
        return render(self.request, 'checkout.html', context ) 


class OrderSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, complete = False)
            context = {'order':order}
            return render(self.request, 'order_summary.html', context )

        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not havean active order..')
            return redirect('/')

        

def payment(request):
    context = {}
    return render(request, 'payment.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        message_body = f'''Hey, I am {name}.My phone number is {phone}.

        {message}
        '''
        # send an email 
        send_mail(
            f'Message from {name} ',
            message_body,
            email,
            ['testerwebsite007@gmail.com'],
            fail_silently=False,
        )
        context = {'name':name}
    else:
        context = {}
    return render(request, 'contact.html', context)


def service(request):
    context = {}
    return render(request, 'service.html', context)



class ShopView(ListView):
    model = Product
    template_name = 'shop.html'


class ProductsView(ListView):
    model = Product
    template_name = 'product.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'single.html'


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        complete=False
    )
    order_qs = Order.objects.filter(user=request.user, complete=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('website:order-summary')
        else:
            
            order.products.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect('website:order-summary')
    else:
        order = Order.objects.create(user= request.user)
        order.products.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('website:order-summary')

    #         messages.info(request, "This item quantity was updated.")
    #         return redirect("website:order-summary")
    #     else:
    #         order.items.add(order_item)
    #         messages.info(request, "This item was added to your cart.")
    #         return redirect("website:order-summary")
    # else:
    #     ordered_date = timezone.now()
    #     order = Order.objects.create(
    #         user=request.user, ordered_date=ordered_date)
    #     order.items.add(order_item)
    #     messages.info(request, "This item was added to your cart.")
    #     return redirect("website:order-summary")

@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        complete=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                complete=False
            )[0]
            order.products.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.") 
            return redirect('website:order-summary')
            
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('website:single',slug=slug )
    else:
        messages.info(request, "You do not have an active order")
        return redirect('website:single',slug=slug )


@login_required
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        complete=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                complete=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.products.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("website:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("website:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("website:product", slug=slug)