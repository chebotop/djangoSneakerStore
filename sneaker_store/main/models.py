from django.db import models
from django.contrib import admin
import json

class ShoeBrand(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ShoeSize(models.Model):
    euro_size = models.CharField(max_length=10)
    sm_size = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.euro_size


    
class ShoeModel(models.Model):
    model = models.CharField(max_length=45)
    price = models.IntegerField()
    desc = models.TextField()
    brand = models.ForeignKey(ShoeBrand, related_name='models', on_delete=models.CASCADE, max_length=45)
    image = models.ImageField(upload_to='gallery', default='')
    sizes = models.ManyToManyField(ShoeSize, related_name='sizes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.model 

def shoe_image_directory_path(instance, filename):
    return f'images/{instance.shoe_model.model}/{filename}'

class ShoeImage(models.Model):
    shoe_model = models.ForeignKey(ShoeModel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=shoe_image_directory_path)

    def __str__(self):
        return f'Image for {self.shoe_model.model}'


class Cart(models.Model):
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class CartItem(models.Model):
    shoe = models.ForeignKey(ShoeModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1) 
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    size = models.CharField(max_length=45, default='')

class Address(models.Model):
    address = models.CharField(max_length=45)
    address2 = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    zipcode = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=60)
    address = models.ForeignKey(Address, related_name="user", on_delete=models.CASCADE)

class Order(models.Model):
    status = models.CharField(max_length=45)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    # credit_card = models.ForeignKey(CreditCard, related_name="orders", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
