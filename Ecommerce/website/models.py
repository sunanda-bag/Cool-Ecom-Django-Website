from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.shortcuts import reverse
from django.conf import settings


CATEGORY_CHOICES = (
    ('C1', 'Category 1'),
    ('C2', 'Category 2'),
    ('C3', 'Category 3')
)

LABEL_CHOICES = (
    ('L1', 'primary'),
    ('L2', 'secondary'),
    ('L3', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)



class Product(models.Model):
    title = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("website:single", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("website:add_to_cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("website:remove_from_cart", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    quantity =  models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    def get_total_item_discount_price(self):
        total = self.product.discount_price * self.quantity
        return total

    def get_total_item_price(self):
        total = self.product.price * self.quantity
        return total

    def get_amount_saved(self):
        total = float(self.get_total_item_price()) - float(self.get_total_item_discount_price())
        return total

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)
    products = models.ManyToManyField(OrderItem)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    

    def __str__(self):
        return str(self.id)

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        return total



'''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''




class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    full_name = models.CharField(max_length=50, null=True)
    mobile_num = models.CharField(max_length=12, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=20, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
