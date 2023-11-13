from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=45)


class Size(models.Model):
    size_value = models.CharField(max_length=12)

    class Meta:
        db_table = 'main_size'
        
    def __str__(self):
        return self.size_value


class ShoeModel(models.Model):
    model = models.CharField(max_length=45)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    desc = models.TextField()
    brand = models.ForeignKey(Brand, related_name="models", on_delete=models.CASCADE)
    color = models.CharField(max_length=45, default='')
    image = models.ImageField(upload_to='gallery', default='')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


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


class CreditCard(models.Model):
    number = models.IntegerField()
    security_code = models.IntegerField()
    expiration_date = models.DateField()
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    address = models.ForeignKey(Address, related_name="card", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="credit_cards", on_delete = models.CASCADE)


class Order(models.Model):
    status = models.CharField(max_length=45)
    cart = models.OneToOneField(
        Cart,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    credit_card = models.ForeignKey(CreditCard, related_name="orders", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)