from django import forms
from .models import Coffee, Trappuccino, Cake, Sandwich, Order, OrderItem, CartItem, Cart, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Profile
        fields = ['address','phone']

class OrderForm(forms.ModelForm):
    coffee = forms.ModelChoiceField(queryset=Coffee.objects.all(), empty_label='Select Coffee')
    trap = forms.ModelChoiceField(queryset=Trappuccino.objects.all(), empty_label='Select Trappuccino')
    cake = forms.ModelChoiceField(queryset=Cake.objects.all(), empty_label='Select Cake')
    sand = forms.ModelChoiceField(queryset=Sandwich.objects.all(), empty_label='Select Sandwich')
    class Meta:
        model = Order
        fields = ['coffee','trap','sand','cake']
       