from django.urls import path,include
# from . import views
from .views import (
    Index,
    SignUp,
    Login,
    Logout,
    CartOrder,
    # Product_List,
    ProductDisplay,
    # ProductView,
    ProductDetailView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
)

# app_name = 'app'

urlpatterns = [
    # path("",views.Index,name="index"),
    # path("signup/",views.SignUp,name="signup"),
    # path("login/",views.Login,name="login"),
    # path("logout/",views.Logout,name="logout"),
    # path("products/",views.Product_List,name="products"),
    # path("cart/",views.Cart,name="cart"),
    # path('',Index,name="index"),
    path('signup/',SignUp,name="signup"),
    path('login/',Login,name="login"),
    path('logout/',Logout,name="logout"),
    path('cartorder/',CartOrder.as_view(),name="cartorder"),
    # path('productlist/',Product_List,name="productlist"),
    path('productdisplay/',ProductDisplay,name="productdisplay"),
    path('',Index.as_view(),name="index"),
    path('productdetailview/<slug>/',ProductDetailView.as_view(),name="productdetailview"),
    path('add_to_cart/<slug>/',add_to_cart,name="add_to_cart"),
    path('remove_from_cart/<slug>/',remove_from_cart,name="remove_from_cart"),
    path('remove_single_item_from_cart/<slug>/',remove_single_item_from_cart,name="remove_single_item_from_cart"),
]