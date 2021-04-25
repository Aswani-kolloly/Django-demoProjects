from django.shortcuts import render,redirect
from .models import Brands,Mobile, Orders
from .forms import BrandCreateForm,ProductForm, UserRegistForm, OrderForm
from  django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth import login,logout

# Create your views here.
def admin_permission_required(func):
    def wrapper(req,**kwargs):
        if not req.user.is_superuser:
            return redirect("error-page")
        else:
            return func(req,**kwargs)
    return wrapper

def error_page(req):
    return render(req,"mobile/errorpage.html")

def user_registration(req):
    form=UserRegistForm()
    context={}
    context["form"]=form
    if req.method=="POST":
        form=UserRegistForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            print("invalid")
            form=UserRegistForm(req.POST)
            context["form"]=form
            return render(req, "mobile/userRegistration.html",context)
    return render(req,"mobile/userRegistration.html",context)

def login_view(req):

    if req.method=="POST":
        uname=req.POST.get("username")
        pswd = req.POST.get("pass")
        user=authenticate(req,username=uname,password=pswd)
        if user:
            print("login success")
            login(req,user)
            return redirect("brands")
        else:
            print("failed")
    return render(req,"mobile/userLogin.html")

def user_logout(req):
    logout(req)
    return redirect("brandsList")

def brands_list(req):
    brands = Brands.objects.all()
    context = {}
    context["brands"] = brands
    return render(req, "mobile/index.html", context)

def product_list(req,brand):

    products = Mobile.objects.all().filter(brand=brand)
    brands = Brands.objects.get(id=brand)
    context = {}
    context["products"] = products
    context["brands"] = brands
    return render(req, "mobile/product_list.html", context)

@admin_permission_required
def product_edit(req,id):
    prod = Mobile.objects.get(id=id)
    form = ProductForm(instance=prod)
    context = {}
    context["form"] = form
    context["form_heading"]="Edit Details"
    context["btn_caption"]="Update"
    if req.method == "POST":
        form = ProductForm(req.POST,req.FILES, instance=prod)
        if form.is_valid():
            form.save()
            return redirect("products")
    return render(req, "mobile/product.html", context)

@admin_permission_required
def product_delete(req,id):
    prod = Mobile.objects.get(id=id)
    prod.delete()
    return redirect("products")


@admin_permission_required
def brand_create(req):

    form = BrandCreateForm()
    context = {}
    context["form"] = form
    brands = Brands.objects.all()
    context["brands"] = brands
    context["form_heading"] = "Register Brands Here !"
    context["btn_caption"] = "Create"
    if req.method == "POST":
        form = BrandCreateForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect("brands")
        else:
            form = BrandCreateForm(req.POST)
            context["form"] = form
            return render(req, "mobile/brandCreate.html", context)
    return render(req, "mobile/brandCreate.html", context)

@admin_permission_required
def brand_edit(req, id):
    brand = Brands.objects.get(id=id)
    form = BrandCreateForm(instance=brand)
    context = {}
    context["form"] = form
    context["form_heading"]="Edit Details"
    context["btn_caption"]="Update"
    if req.method == "POST":
        form = BrandCreateForm(req.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect("brands")
    return render(req, "mobile/brandCreate.html", context)

@admin_permission_required
def brand_delete(req,id):

    brand = Brands.objects.get(id=id)
    brand.delete()
    return redirect("brands")


@admin_permission_required
def product_create(req):
    form = ProductForm()
    context = {}
    context["form"] = form
    products = Mobile.objects.all()
    context["products"] = products
    context["form_heading"] = "Register Products Here !"
    context["btn_caption"] = "Create"

    if req.method == "POST":
        form = ProductForm(req.POST,req.FILES)
        if form.is_valid():
            form.save()
            return redirect("products")
        else:
            form = ProductForm(req.POST)
            context["form"] = form
            return render(req, "mobile/product.html", context)
    return render(req, "mobile/product.html", context)

def order_items(req,id):
    if req.user.is_authenticated:
        product = Mobile.objects.get(id=id)
        form = OrderForm(initial={"product":product})
        context = {}
        context["form"] = form
        if req.method == "POST":
            form = OrderForm(req.POST)
            if form.is_valid():
                form.save()
                return redirect("cart-items")
        return render(req, "mobile/orderPage.html", context)
    else:
        return redirect("login")

def cart(req):
    if req.user.is_authenticated:
        userna = req.user
        #print(userna)
        orders = Orders.objects.all().filter(user=userna).exclude(status="cancelled")
        tot=0
        for x in orders:
            tot+=x.product.price
        context = {}
        context["orders"] = orders
        context["total"]=tot
        return render(req, "mobile/cartPage.html",context)
    else:
        return redirect("login")

@admin_permission_required
def view_orders(req):
    context = {}
    orders = Orders.objects.all().exclude(status="cancelled")
    context["orders"] = orders
    if req.method == "POST":
        print("post req")
    return render(req, "mobile/orders_list.html", context)

@admin_permission_required
def order_approve(req,id):
    Orders.objects.filter(id=id).update(status="dispatched")
    orders = Orders.objects.all()
    context = {}
    context["orders"] = orders
    return redirect(req.META.get('HTTP_REFERER'))


def order_cancel(req,id):
    if req.user.is_authenticated:
        orders = Orders.objects.all()
        context = {}
        context["orders"] = orders
        Orders.objects.filter(id=id,user=req.user).update(status="cancelled")
        return redirect("cart-items")
    else:
        return redirect("login")







