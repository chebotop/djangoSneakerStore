from django.db import models
from django.contrib import admin
import json

class ShoeBrand(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

<<<<<<< HEAD

class ShoeSize(models.Model):
    euro_size = models.CharField(max_length=10)
    sm_size = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.euro_size
=======

    


# class ShoeSize(models.Model):
#     euro_size = models.CharField(max_length=20)
#     sm_size = models.CharField(max_length=20)
#     gender = models.CharField(max_length=20)

def default_size():
    return {
        "women": {
            "36EUR": "22.5см",
            "37EUR": "23.5см",
            "38EUR": "24см",
            "39EUR": "25см",
            "40EUR": "25.5см",
        },
        "men": {
            "41EUR": "26см",
            "42EUR": "26.5см",
            "43EUR": "27.5см",
            "44EUR": "28см",
            "45EUR": "29см"
        }
    }
>>>>>>> 399bc5d090769e750f9502be8a936b2f2f60f4c3

class ShoeSize(models.Model):
    size = models.CharField(max_length=20)

    def __str__(self):
        return self.size
    
class ShoeModel(models.Model):
    model = models.CharField(max_length=45)
    price = models.IntegerField()
    desc = models.TextField()
    brand = models.ForeignKey(ShoeBrand, related_name='models', on_delete=models.CASCADE, max_length=45)
    image = models.ImageField(upload_to='gallery', default='')
<<<<<<< HEAD
    sizes = models.ManyToManyField(ShoeSize)
=======
    sizes = models.ManyToManyField(ShoeSize, related_name='sizes')
    # sizes = models.ManyToManyField(ShoeSize)
>>>>>>> 399bc5d090769e750f9502be8a936b2f2f60f4c3
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.model 

def shoe_image_directory_path(instance, filename):
    return f'images/{instance.shoe_model.model}/{filename}'

class ShoeImage(models.Model):
    shoe_model = models.ForeignKey(ShoeModel, related_name='images', on_delete=models.CASCADE)
    extra_images = models.ImageField(upload_to=shoe_image_directory_path)

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
