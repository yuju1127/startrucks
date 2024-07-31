from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Cake(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    images = models.ImageField(upload_to='cakes/')

    def __str__(self):
        return self.name
    
class Coffee(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    images = models.ImageField(upload_to='cakes/')

    def __str__(self):
        return self.name

class Sandwich(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    images = models.ImageField(upload_to='cakes/')

    def __str__(self):
        return self.name
    
class Trappuccino(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    images = models.ImageField(upload_to='cakes/')

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coffees = models.ManyToManyField(Coffee, through='CartItem')
    traps = models.ManyToManyField(Trappuccino, through='CartItem')
    cakes = models.ManyToManyField(Cake, through='CartItem')
    sands = models.ManyToManyField(Sandwich, through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    coffees = models.ForeignKey(Coffee,on_delete=models.CASCADE,null=True,blank=True)
    coffees_quantity = models.PositiveIntegerField(default=0)
    trappuccinos = models.ForeignKey(Trappuccino,on_delete=models.CASCADE,null=True,blank=True)
    traps_quantity = models.PositiveIntegerField(default=0)
    cakes = models.ForeignKey(Cake,on_delete=models.CASCADE,null=True,blank=True)
    cakes_quantity = models.PositiveIntegerField(default=0)
    sandwiches = models.ForeignKey(Sandwich,on_delete=models.CASCADE,null=True,blank=True)
    sands_quantity = models.PositiveIntegerField(default=0)

    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cakes = models.ManyToManyField(Cake,through='OrderItem')
    coffees = models.ManyToManyField(Coffee,through='OrderItem')
    traps = models.ManyToManyField(Trappuccino,through='OrderItem')
    sands = models.ManyToManyField(Sandwich,through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True) #確認新增的字段

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    coffees = models.ForeignKey(Coffee,on_delete=models.CASCADE)
    coffees_quantity = models.PositiveIntegerField()
    trappuccinos = models.ForeignKey(Trappuccino,on_delete=models.CASCADE)
    traps_quantity = models.PositiveIntegerField(default=0)
    cakes = models.ForeignKey(Cake,on_delete=models.CASCADE)
    cakes_quantity = models.PositiveIntegerField(default=0)
    sandwiches = models.ForeignKey(Sandwich,on_delete=models.CASCADE)
    sands_quantity = models.PositiveIntegerField()
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
    