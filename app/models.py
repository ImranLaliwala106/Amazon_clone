from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser

# Create your models here.
CATEGORY_CHOICES =(
    ('M', "Men's Fashion"),
    ('F', "Women's Fashion"),
    ('E', "Electronics"),
    ('MO', "Mobiles")
)

LABEL_CHOICES =(
    ('D', "Deal of the Day"),
    ('B', "Best Seller"),
    ('O', "Off")
)

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=50)
    original_price = models.FloatField()
    discount_pr = models.IntegerField(blank=True,null=True)
    price = models.FloatField()
    pic = models.ImageField(upload_to="static/images")
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    label = models.CharField(choices=LABEL_CHOICES,max_length=1)
    desc = models.TextField(max_length=5000 ,default=None)
    slug = models.SlugField()

    def __str__(self):
        return self.name
    
    def product_pic(self):
        return mark_safe('<img src="{}"width="100" height="100"/>'.format(self.pic.url))

    def get_absolute_url(self):
        return reverse("productdetailview",kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add_to_cart",kwargs={
            'slug': self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("remove_from_cart",kwargs={
            'slug': self.slug
        })
    
class ProductOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.products.name}"
    
    def get_total_product_price(self):
        return self.quantity * self.products.original_price
    
    def get_total_discount_price(self):
        return self.quantity * self.products.price
    
    def get_total_price(self):
        if self.products.discount_pr:
            return self.get_total_discount_price()
        else:
            return self.get_total_product_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductOrder)
    ordered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username
    
    def get_subtotal(self):
        total = 0
        for product_order in self.products.all():
            total += product_order.get_total_price()
        return total
