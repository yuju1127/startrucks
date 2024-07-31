from django.contrib import admin
from .models import Cake, Coffee, Trappuccino, Sandwich, Cart, CartItem, Order, OrderItem
# Register your models here.

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ['name','price']
    search_fields = ('name',)

@admin.register(Coffee)
class CoffeAdmin(admin.ModelAdmin):
    list_display = ['name','price']
    search_fields = ('name',)

@admin.register(Trappuccino)
class TrapAdmin(admin.ModelAdmin):
    list_display = ['name','price']
    search_fields = ('name',)

@admin.register(Sandwich)
class SandAdmin(admin.ModelAdmin):
    list_display = ['name','price']
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','total_price','created_at')
