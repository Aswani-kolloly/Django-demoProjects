from django.db import models

# Create your models here.
class Brands(models.Model):
    brand_name=models.CharField(max_length=120,unique=True)
    def __str__(self):
        return self.brand_name

class Mobile(models.Model):
    mobile_name=models.CharField(max_length=120)
    brand=models.ForeignKey(Brands,on_delete=models.CASCADE)
    price=models.IntegerField(null=False)
    model_name=models.CharField(max_length=80)
    specs=models.CharField(max_length=250)
    desc=models.CharField(max_length=120)
    image=models.ImageField(upload_to='images')

    def __str__(self):
        return self.mobile_name
class Orders(models.Model):
    product = models.ForeignKey(Mobile, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    user = models.CharField(max_length=120)
    choices = [
        (" ordered ", "ordered"),
        ("dispatched", "dispatched"),
        ("cancelled", "cancelled")
    ]
    status = models.CharField(max_length=10,choices=choices,default="ordered")


