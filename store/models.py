from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class FilterPrice(models.Model):
    price = models.CharField(max_length=50)

    def __str__(self):
        return self.price

class Product(models.Model):
    STATUS = (
        ('Publish', 'Publish'),
        ('Draft', 'Draft'),
    )

    CONDITION = (
        ('New', 'New'),
        ('Old', 'Old'),
    )

    name = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to='product_images/')
    status = models.CharField(max_length=200, choices=STATUS, default='Publish')
    condition = models.CharField(max_length=100, choices=CONDITION, default='New')
    information = RichTextField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    filter_price = models.ForeignKey(FilterPrice, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Images(models.Model):
    image = models.ImageField(upload_to='product_images/images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    amount = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    # --- CAMPO NUEVO AÑADIDO ---
    payment_id = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to='order_images/')
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=1000)

    def __str__(self):
        return self.order.user.username