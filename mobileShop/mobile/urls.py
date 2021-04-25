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
from .views import Brands_list, Brand_create, Brand_edit, Brand_delete, User_login, user_logout, User_registration, Product_create, Product_edit, Product_delete, error_page, Products_list, Order_item, Cart, Order_cancel, View_orders, Order_approve


urlpatterns = [
    path("", Brands_list.as_view(),name="brandsList"),
    path("login", User_login.as_view(), name="userLogin"),
    path("user-registration", User_registration.as_view(), name="userRegistration"),
    path("logout", user_logout, name="userLogout"),
    path("brands", Brand_create.as_view(), name="brands"),
    path("brands/edit/<int:pk>", Brand_edit.as_view(), name="editBrand"),
    path("brands/delete/<int:pk>", Brand_delete.as_view(), name="deleteBrand"),
    path("products", Product_create.as_view(), name="products"),
    path("products/edit/<int:pk>", Product_edit.as_view(), name="editProduct"),
    path("products/delete/<int:pk>", Product_delete.as_view(), name="deleteProduct"),
    path("listProducts/<int:brand>", Products_list.as_view(), name="listProducts"),
    path("order-items/<int:pk>", Order_item.as_view(), name="order-items"),
    path("orders/cancel/<int:pk>", Order_cancel.as_view(),name="cancel-order"),
    path("orders/approve/<int:pk>", Order_approve.as_view(),name="order-approve"),
    path("orders", View_orders.as_view(), name="orders"),
    path("cart-items", Cart.as_view(), name="cart-items"),
    path("error", error_page, name="error-page")

]
#  request:render(request, "mobile/index.html")
