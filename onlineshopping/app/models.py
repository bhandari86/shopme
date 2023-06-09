from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
STATE_CHOICES =(
    
    ('Kathmandu','Kathmandu'),
    ('Lalitpur','Lalitpur'),
    ('Bhaktapur','Bhaktapur'),
    ('banepa','Banepa'),
    ('Butwol','Butwol'),
)

class Customer(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality =models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    
    def __str__(self):
        return str(self.id)
    
CATEGORY_CHOICES = (
    ('M','Male'),
    ('W','Women'),
    ('S','Shoes'),
    ('SM','Men Shoes'),
    ('SW',' Wonem Shoes'),
)
class Product(models.Model):
    title= models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price= models.FloatField()
    description = models.TextField()
    brand= models.CharField(max_length=200)
    category = models.CharField(choices= CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to= 'productimage')
    
    
    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
    
STATUS_CHOICES=(
    ('out of Stock','Out of Stock'),
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50, choices=STATUS_CHOICES,default ='pending')
    payment_method=models.CharField(max_length=50,default ='khalti')
    paid = models.BooleanField(default=False, null=True)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
class TOPSALE(models.Model):
    title= models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price= models.FloatField()
    description = models.TextField()
    brand= models.CharField(max_length=200)
    product_image = models.ImageField(upload_to= 'productimage')
    

    def __str__(self):
        return str(self.id)
   

class Main_Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    main_category = models.ForeignKey(Main_Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " -- " + self.main_category.name

class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.category.main_category.name + " -- " + self.category.name + " -- " + self.name
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)