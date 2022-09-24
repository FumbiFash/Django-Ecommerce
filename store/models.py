
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# class Room(models.Model):

    
class User(AbstractUser):
    name =   models.CharField(max_length=200,null = True)
    email = models.EmailField(max_length=200,unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Category(models.Model):
    name = models.CharField(max_length = 200,null=True)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length= 250,null=True)
    email = models.CharField(max_length=250, null = True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length = 250)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    digital = models.BooleanField(default = False, null = True, blank = True)
    image = models.ImageField(null = True, blank = True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null = True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank = False, null =True)
    transaction_id = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitem = self.orderitem_set.all()
        for i in orderitem:
            if i.product.digital == False:
                shipping = True
        return shipping
            

    # get total cost of items in cart
    @property
    def get_cart_total(self): 
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    # get total number of items in cart
    @property
    def get_cart_items(self): 
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete = models.SET_NULL, null=True)
    address = models.CharField(max_length=250,null = False)
    city = models.CharField(max_length = 250,null = False)
    state = models.CharField(max_length=200,null=False)
    zipcode = models.CharField(max_length = 250, null = False)

    def __str__(self):
        return self.address

   

    