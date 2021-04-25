from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Brands, Mobile, Orders
from django import forms

class UserRegistForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","first_name","last_name","email","password1","password2"]

class BrandCreateForm(ModelForm):
    class Meta:
        model=Brands
        fields='__all__'

class ProductForm(ModelForm):
    class Meta:
        model=Mobile
        fields='__all__'

class OrderForm(ModelForm):
    #product = forms.CharField(max_length=50)
    class Meta:
        model = Orders
        fields = ['product','user', 'address' ]

