from django.db import models
import json

class ShoeBrand(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name 

class ShoeColor(models.Model):
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.color 


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


class ShoeModel(models.Model):
    model = models.CharField(max_length=45)
    price = models.IntegerField()
    desc = models.TextField()
    brand = models.ForeignKey(ShoeBrand, related_name='models', on_delete=models.CASCADE, max_length=45)
    color = models.ForeignKey(ShoeColor, max_length=45, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery', default='')
    sizes = models.JSONField(default=default_size)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.model 


class Cart(models.Model): 
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class CartItem(models.Model):
    shoe = models.ForeignKey(ShoeModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

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







# class CreditCard(models.Model):
#     number = models.IntegerField()
#     security_code = models.IntegerField()
#     expiration_date = models.DateField()
#     first_name = models.CharField(max_length=45)
#     last_name = models.CharField(max_length=45)
#     address = models.ForeignKey(Address, related_name="card", on_delete = models.CASCADE)
#     user = models.ForeignKey(User, related_name="credit_cards", on_delete = models.CASCADE)


