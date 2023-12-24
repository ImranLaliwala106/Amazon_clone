from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import ListView,DetailView,View
from .forms import CustomUserCreationForm
from .models import Product,ProductOrder,Order
from django.utils import timezone
# Create your views here.

# def Index(request):
#     return render(request,"app/index.html")

def SignUp(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # user.save()
            messages.success(request,"User created successfully!")
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request,'app/registration/signup.html', {'form': form})

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfull!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request,'app/registration/login.html')

def Logout(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('index')

class Index(ListView):
    model = Product
    paginate_by = 8
    template_name = "app/index.html"

# class ProductView(ListView):
#     model = Product
#     template_name = "app/product_list.html"

class ProductDetailView(DetailView):
    model = Product
    template_name = "app/product_detail.html"  

def ProductDisplay(request):
    context = {
        'products' : Product.objects.all()
    }
    return render(request,'app/product_detail.html', context)

# def Product_List(request):
#     context = {
#         'products' : Product.objects.all()
#     }
#     return render(request,'app/product_list.html', context)

@login_required
def add_to_cart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    product_order,created = ProductOrder.objects.get_or_create(
        products=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(products__slug=product.slug).exists():
            product_order.quantity += 1
            product_order.save()
            messages.info(request,"Product quantity updated")
            return redirect("cartorder")
        else:
            order.products.add(product_order)
            messages.info(request,"Product added to cart")
            return redirect("cartorder")
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=order_date)
        order.products.add(product_order)
        messages.info(request,"Product added to cart")
    return redirect("cartorder")

@login_required    
def remove_from_cart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(products__slug=product.slug).exists():
            product_order = ProductOrder.objects.filter(
                products=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(product_order)
            messages.info(request,"Product removed from cart")
            return redirect("cartorder")
        else:
            messages.info(request,"Cart was empty")
            return redirect("productdetailview",slug=slug) 
    else:
        messages.info(request,"Cart empty")
        return redirect("productdetailview",slug=slug)                

# @login_required    
# def remove_single_item_from_cart(request,slug):
#     product = get_object_or_404(Product,slug=slug)
#     order_qs = Order.objects.filter(
#         user=request.user, 
#         ordered=False
#         )
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order product is in the order
#         if order.products.filter(products__slug=product.slug).exists():
#             product_order = ProductOrder.objects.filter(
#                 products=product,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             product_order.quantity -= 1
#             product_order.save()
#             messages.info(request,"Product quantity updated")
#             return redirect("cartorder")
#         else:
#             messages.info(request,"Cart was empty")
#             return redirect("productdetailview",slug=slug) 
#     else:
#         messages.info(request,"Cart empty")
#         return redirect("productdetailview",slug=slug)

@login_required    
def remove_single_item_from_cart(request,slug):
    product = get_object_or_404(Product,slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(products__slug=product.slug).exists():
            product_order = ProductOrder.objects.filter(
                products=product,
                user=request.user,
                ordered=False
            )[0]
            if product_order:
                # Check if quantity is already at 1 before decrementing
                if product_order.quantity > 1:
                    product_order.quantity -= 1
                    product_order.save()
                    messages.info(request,"Product quantity updated")
                    return redirect("cartorder")
                else:
                    # If quantity is already 1, remove the item from the cart
                    product_order.delete()
                    messages.info(request, "Product removed from the cart")
                    return redirect("cartorder")
        # If the product is not in the order        
        else:
            messages.info(request,"Cart was empty")
            return redirect("productdetailview",slug=slug) 
    # If the cart is empty    
    else:
        messages.info(request,"Cart empty")
        return redirect("productdetailview",slug=slug)  
        
class CartOrder(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "app/cart.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request,'You do not have an active order')
            return redirect("/")
            