from django.contrib import admin
from .forms import CustomUserCreationForm
from .models import CustomUser, Product, ProductOrder,Order

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    list_display = ['username','email']

class ProductList(admin.ModelAdmin):
    list_display = ('name','category','price','product_pic')

class OrderList(admin.ModelAdmin):
    list_display = ('products','quantity')

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(ProductOrder,OrderList)
admin.site.register(Product, ProductList)
admin.site.register(Order)
