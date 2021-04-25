from django.shortcuts import render,redirect
from .models import Brands, Mobile, Orders
from .forms import BrandCreateForm, UserRegistForm, ProductForm, OrderForm
from  django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.contrib.auth import login,logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Create your views here.
def admin_permission_required(func):
    def wrapper(req,**kwargs):
        if not req.user.is_superuser:
            return redirect("error-page")
        else:
            return func(req,**kwargs)
    return wrapper

class User_registration(TemplateView):
    template_name = "mobile/userRegistration.html"
    context = {}
    form_class = UserRegistForm

    def get(self, req, *args, **kwargs):
        self.context["form"] = self.form_class()
        return render(req, self.template_name, self.context)

    def post(self, req, *args, **kwargs):
        form = self.form_class(req.POST)
        if form.is_valid():
            form.save()
            return redirect("brandsList")
        else:
            self.context["form"] = form
            return render(req, self.template_name, self.context)

class User_login(TemplateView):
    template_name = "mobile/userLogin.html"

    def get(self,req,*args, **kwargs):
        return render(req,self.template_name)

    def post(self,req, *args, **kwargs):
        uname = req.POST.get("username")
        pswd = req.POST.get("pass")
        user = authenticate(req, username=uname, password=pswd)
        if user:
            print("login success")
            login(req, user)
            return redirect("brandsList")
        else:
            print("failed")
        return render(req,self.template_name)

def user_logout(req):
    logout(req)
    return redirect("brandsList")

def error_page(req):
    return render(req,"mobile/errorpage.html")

class Brands_list(TemplateView):
    model = Brands
    template_name = "mobile/index.html"
    context = {}
    def get(self,req, *args, **kwargs):
        brands = self.model.objects.all()
        self.context["brands"] = brands
        return render(req, self.template_name, self.context)

@method_decorator(admin_permission_required,name='dispatch')
class Brand_create(TemplateView):

    model = Brands
    template_name = "mobile/brandCreate.html"
    context = {}
    form_class = BrandCreateForm

    def get(self,req,*args, **kwargs):
        self.context["form"] = self.form_class()
        brands = self.model.objects.all()
        self.context["brands"] = brands
        self.context["form_heading"] = "Register Brands Here !"
        self.context["btn_caption"] = "Create"
        return render(req,self.template_name,self.context)
    def post(self,req, *args, **kwargs):
        form = self.form_class(req.POST)
        if form.is_valid():
            form.save()
            return redirect("brands")
        else:
            self.context["form"] = form
            return render(req,self.template_name,self.context)

@method_decorator(admin_permission_required,name='dispatch')
class Brand_edit(TemplateView):
    model = Brands
    template_name = "mobile/brandCreate.html"
    form_class = BrandCreateForm
    context = {}
    def get_object(self,id):
        return self.model.objects.get(id=id)
    def get(self,req, *args, **kwargs):
        brand = self.get_object(kwargs["pk"])
        form = self.form_class(instance=brand)
        self.context["form"] =  form
        self.context["form_heading"] = "Edit Brands Here !"
        self.context["btn_caption"] = "Edit"
        return render(req,self.template_name,self.context)
    def post(self,req,*args, **kwargs):
        brand = self.get_object(kwargs["pk"])
        form = self.form_class(req.POST,instance=brand)
        if form.is_valid():
            form.save()
            return redirect("brands")
        else:
            self.context["form"] = form
            return render(req,self.template_name,self.context)

@method_decorator(admin_permission_required,name='dispatch')
class Brand_delete(TemplateView):
    model = Brands
    def get(self,req, *args, **kwargs):
        brand = self.model.objects.get(id=kwargs["pk"])
        brand.delete()
        return redirect("brands")

class Products_list(TemplateView):
    model = Mobile
    template_name = "mobile/product_list.html"
    context = {}
    def get(self,req, **kwargs):
        products = self.model.objects.all().filter(brand=kwargs["brand"])
        brand = Brands.objects.get(id=kwargs["brand"])
        self.context["products"] = products
        self.context["brands"] = brand
        return render(req, self.template_name, self.context)

@method_decorator(admin_permission_required,name='dispatch')
class Product_create(TemplateView):

    model = Mobile
    template_name = "mobile/product.html"
    context = {}
    form_class = ProductForm

    def get(self,req,*args, **kwargs):
        self.context["form"] = self.form_class()
        products = self.model.objects.all()
        self.context["products"] = products
        self.context["form_heading"] = "Register Products Here !"
        self.context["btn_caption"] = "Create"
        return render(req,self.template_name,self.context)
    def post(self,req, *args, **kwargs):
        form = self.form_class(req.POST,req.FILES)
        if form.is_valid():
            form.save()
            return redirect("products")
        else:
            self.context["form"] = self.form_class(req.POST)
            return render(req,self.template_name,self.context)

@method_decorator(admin_permission_required,name='dispatch')
class Product_edit(TemplateView):
    model = Mobile
    template_name = "mobile/product.html"
    form_class = ProductForm
    context = {}
    def get_object(self,id):
        return self.model.objects.get(id=id)
    def get(self,req, *args, **kwargs):
        product = self.get_object(kwargs["pk"])
        form = self.form_class(instance=product)
        self.context["form"] =  form
        self.context["form_heading"] = "Edit Products Here !"
        self.context["btn_caption"] = "Edit"
        return render(req,self.template_name,self.context)
    def post(self,req,*args, **kwargs):
        product = self.get_object(kwargs["pk"])
        form = self.form_class(req.POST, req.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("products")
        else:
            self.context["form"] = form
            return render(req,self.template_name,self.context)

@method_decorator(admin_permission_required,name='dispatch')
class Product_delete(TemplateView):
    model = Mobile
    def get(self,req, *args, **kwargs):
        prod = self.model.objects.get(id=kwargs["pk"])
        prod.delete()
        return redirect("products")

@method_decorator(login_required(login_url='userLogin'),name='dispatch')
class Order_item(TemplateView):
    model = Mobile
    template_name = "mobile/orderPage.html"
    context = {}
    form_class = OrderForm
    def get(self,req, *args, **kwargs):
        product = self.model.objects.get(id=kwargs["pk"])
        form = OrderForm(initial={"product": product})
        self.context["form"]=form
        return render(req,self.template_name,self.context)
    def post(self,req,*args,**kwargs):
        form = OrderForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect("cart-items")
        else:
            self.context["form"] = form
            return render(req,self.template_name,self.context)

@method_decorator(login_required(login_url='userLogin'), name='dispatch')
class Order_cancel(TemplateView):
    model = Orders
    def get(self,req,*args,**kwargs):
        self.model.objects.filter(id=kwargs["pk"], user=req.user).update(status="cancelled")
        return redirect("cart-items")

@method_decorator(admin_permission_required,name='dispatch')
class View_orders(TemplateView):
    model = Orders
    template_name = "mobile/orders_list.html"
    context = {}
    def get(self,req,*args,**kwargs):
        orders = self.model.objects.all().exclude(status="cancelled")
        self.context["orders"] = orders
        return render(req,self.template_name,self.context)

@method_decorator(admin_permission_required,name='dispatch')
class Order_approve(TemplateView):
    model = Orders
    def get(self,req,*args,**kwargs):
        self.model.objects.filter(id=kwargs["pk"]).update(status="dispatched")
        return redirect("orders")

@method_decorator(login_required(login_url='userLogin'),name='dispatch')
class Cart(TemplateView):
    model = Orders
    template_name = "mobile/cartPage.html"
    context = {}
    def get(self,req,*args,**kwargs):
        userna = req.user
        # print(userna)
        orders = self.model.objects.all().filter(user=userna).exclude(status="cancelled")
        tot = 0
        for x in orders:
            tot += x.product.price
        self.context["orders"] = orders
        self.context["total"] = tot
        return render(req, self.template_name, self.context)


