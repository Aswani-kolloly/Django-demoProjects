"""mobileApplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .views import brand_create, brand_edit, brand_delete, product_create, product_delete,product_edit, product_list, brands_list, user_registration,login_view, user_logout,order_items, cart, view_orders, order_approve, order_cancel, error_page


urlpatterns = [
    path("", brands_list,name="brandsList"),
    path("login", login_view, name="login"),
    path("user-logout", user_logout, name="user-logout"),
    path("register", user_registration, name="register"),
    path("brands", brand_create, name="brands"),
    path("brands/edit/<int:id>", brand_edit, name="editBrand"),
    path("brands/delete/<int:id>", brand_delete, name="deleteBrand"),
    path("products", product_create, name="products"),
    path("products/edit/<int:id>", product_edit, name="product-edit"),
    path("products/delete/<int:id>", product_delete, name="product-delete"),
    path("listProducts/<int:brand>", product_list, name="listProducts"),
    path("order-items/<int:id>", order_items, name="order-items"),
    path("cart-items", cart, name="cart-items"),
    path("orders", view_orders, name="orders"),
    path("orders/approve/<int:id>",order_approve,name="order-approve"),
    path("orders/cancel/<int:id>",order_cancel,name="order-cancel"),
    path("error", error_page, name="error-page")

]
#  request:render(request, "mobile/index.html")
