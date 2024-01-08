from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
import mptt
import os


class ShoeBrand(MPTTModel):
    class Meta:
        db_table = 'brand'
        ordering = ('tree_id', 'level')
    name = models.CharField(max_length=20)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class ShoeSize(models.Model):
    euro_size = models.CharField(max_length=10)
    sm_size = models.CharField(max_length=10)

    def __str__(self):
        return self.euro_size


class CategoryModel(MPTTModel):
    name = models.CharField(null=True, blank=True, max_length=20, default='')
    parent = models.ForeignKey(ShoeBrand, on_delete=models.CASCADE, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class ShoeModel(MPTTModel):
    name = models.CharField(max_length=45)
    brand = models.ForeignKey(ShoeBrand, related_name='models', on_delete=models.CASCADE, max_length=45)
    parent = models.ForeignKey(CategoryModel, related_name='categories', null=True, blank=True,
                                 on_delete=models.CASCADE, max_length=20, default='')
    price = models.IntegerField()
    desc = models.TextField()
    image = models.ImageField(upload_to='gallery', default='')
    sizes = models.ManyToManyField(ShoeSize, related_name='sizes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


def shoe_image_directory_path(instance, filename):
    directory_path = os.path.join(settings.MEDIA_ROOT, f'images/{instance.shoe_model.name}/')

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_count = len(os.listdir(directory_path))
    new_filename = f'{file_count + 1}.jpg'
    full_path = os.path.join(directory_path, new_filename)
    print(f"Saving file to: {full_path}")

    return os.path.join(f'images/{instance.shoe_model.name}/', new_filename)


class ShoeGalleryImages(models.Model):
    shoe_model = models.ForeignKey(ShoeModel, related_name='shoe_gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=shoe_image_directory_path)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f'Image for {self.shoe_model.name}'

    class Meta:
        ordering = ['my_order']


class Cart(models.Model):
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    shoe = models.ForeignKey(ShoeModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size = models.CharField(max_length=45, default='')


class Address(models.Model):
    address = models.CharField(max_length=45)
    address2 = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    zipcode = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
