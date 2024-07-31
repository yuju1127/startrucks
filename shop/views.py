from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from .models import Coffee,Trappuccino, Sandwich, Cake, Order, Profile, Cart, CartItem,OrderItem
from .forms import ProfileForm, OrderForm
import logging

# Create your views here.

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'shop/index .html')

def cakes(request):
    cakes = Cake.objects.all()
    return render(request, 'shop/cakes.html',{'cakes':cakes})

def coffee(request):
    coffee = Coffee.objects.all()
    return render(request, 'shop/coffee.html',{'coffee':coffee})

def trap(request):
    trap = Trappuccino.objects.all()
    return render(request, 'shop/trap.html',{'trap':trap})

def sand(request):
    sand = Sandwich.objects.all()
    return render(request, 'shop/sand.html',{'sand':sand})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.email = profile_form.cleaned_data.get('email')
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'shop/register.html', {'form':form, 'profile_form':profile_form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/login/')
def order_cakes(request,cakes_id):
    cakes = get_object_or_404(Cake,id=cakes_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart,cakes=cakes)
    cart_item.cakes_quantity+=1
    cart_item.save()
    total_price = (cart_item.cakes.price * cart_item.cakes_quantity)
    order = Order.objects.create(user=request.user, total_price=total_price)
    return redirect('cakes')

@login_required(login_url='/login/')
def order_coffee(request,coffees_id):
    coffee = get_object_or_404(Coffee,id=coffees_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart,coffees=coffee)
    cart_item.coffees_quantity+=1
    cart_item.save()
    total_price = (cart_item.coffees.price * cart_item.coffees_quantity)
    order = Order.objects.create(user=request.user, total_price=total_price)
    return redirect('coffee')

@login_required(login_url='/login/')
def order_sandwich(request,sandwiches_id):
    sandwich = get_object_or_404(Sandwich,id=sandwiches_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart,sandwiches=sandwich)
    cart_item.sands_quantity+=1
    cart_item.save()
    total_price = (cart_item.sandwiches.price * cart_item.sands_quantity)
    order = Order.objects.create(user=request.user, total_price=total_price)
    return redirect('sand')

@login_required(login_url='/login/')
def order_trappuccino(request,trappuccinos_id):
    trappuccino = get_object_or_404(Trappuccino,id=trappuccinos_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart,trappuccinos=trappuccino)
    cart_item.traps_quantity+=1
    cart_item.save()
    total_price = (cart_item.trappuccinos.price * cart_item.traps_quantity)
    order = Order.objects.create(user=request.user, total_price=total_price)
    return redirect('trap')

@login_required
def order_history(request):
    return render(request, 'shop/order_history.html')

@login_required
def order_confirmation(request):
    cart = Cart.objects.get(user=request.user)
    cakes_price = sum(item.cakes.price * item.cakes_quantity for item in cart.cartitem_set.all() if item.cakes)
    coffees_price = sum(item.coffees.price * item.coffees_quantity for item in cart.cartitem_set.all() if item.coffees)
    trappuccinos_price = sum(item.trappuccinos.price * item.traps_quantity for item in cart.cartitem_set.all() if item.trappuccinos)
    sandwiches_price = sum(item.sandwiches.price * item.sands_quantity for item in cart.cartitem_set.all() if item.sandwiches)
    total_price = cakes_price + coffees_price + trappuccinos_price + sandwiches_price
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_confirmation.html', {'cart': cart, 'total_price': total_price,'orders':orders})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form':form})

@login_required
def order_confirm(request, cart_item_id):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem,id=cart_item_id,cart=cart)
        cakes_price = sum(item.cakes.price * item.cakes_quantity for item in cart.cartitem_set.all() if item.cakes)
        coffees_price = sum(item.coffees.price * item.coffees_quantity for item in cart.cartitem_set.all() if item.coffees)
        trappuccinos_price = sum(item.trappuccinos.price * item.traps_quantity for item in cart.cartitem_set.all() if item.trappuccinos)
        sandwiches_price = sum(item.sandwiches.price * item.sands_quantity for item in cart.cartitem_set.all() if item.sandwiches)
        total_price = cakes_price + coffees_price + trappuccinos_price + sandwiches_price
        
        order_details = []
        for item in cart.cartitem_set.all():
            if item.cakes:
                order_details.append(f'{item.cakes_quantity} x {item.cakes.name}')
            if item.coffees:
                order_details.append(f'{item.coffees_quantity} x {item.coffees.name}')
            if item.trappuccinos:
                order_details.append(f'{item.traps_quantity} x {item.trappuccinos.name}')
            if item.sandwiches:
                order_details.append(f'{item.sands_quantity} x {item.sandwiches.name}')
        
        order_details_str = '\n'.join(order_details)
        
        try:
            send_mail(
                'Order Confirmation',
                f'Thank you for your order, {request.user.username}. You have ordered the following items:\n\n'
                 + order_details_str + f'\n\nTotal price: ${total_price:.2f}.',
                'your-email@gmail.com',
                [request.user.email],
                fail_silently=False,
            )
            cart_item.status = 'Confirmed'
            cart_item.save()
            return render(request, 'shop/order_history.html')
        except Exception as e:
            logger.error(f'Error sending email:{e}')
    except ObjectDoesNotExist:
        logger.error('Order does not exist.')
    return redirect('index')

@login_required
def order_increase(request, cart_item_id):
    #獲取用戶購物車
    cart_item = get_object_or_404(CartItem,id=cart_item_id,cart__user=request.user)
    #獲取特定的cartitem
    if cart_item.cakes_quantity >= 1:
        cart_item.cakes_quantity += 1
    elif cart_item.coffees_quantity >= 1:
        cart_item.coffees_quantity += 1
    elif cart_item.traps_quantity >= 1:
        cart_item.traps_quantity += 1
    elif cart_item.sands_quantity >= 1:
        cart_item.sands_quantity += 1
    cart_item.save()
    return redirect('order_confirmation')

@login_required
def order_decrease(request, cart_item_id):
    #獲取用戶購物車
    cart_item = get_object_or_404(CartItem,id=cart_item_id,cart__user=request.user)
    #獲取特定的cartitem
    if cart_item.cakes_quantity > 1:
        cart_item.cakes_quantity -= 1
    elif cart_item.coffees_quantity > 1:
        cart_item.coffees_quantity -= 1
    elif cart_item.traps_quantity > 1:
        cart_item.traps_quantity -= 1
    elif cart_item.sands_quantity > 1:
        cart_item.sands_quantity -= 1
    if cart_item.cakes_quantity==0 and cart_item.coffees_quantity==0 and cart_item.traps_quantity==0 and cart_item.sands_quantity==0 :
        cart_item.delete()
    else:
        cart_item.save()
    return redirect('order_confirmation')

@login_required
def order_delete(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('order_confirmation')


@login_required
def add_item_to_order(request, order_id):
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = request.user
            new_order.status = 'Pending'
            new_order.save()
    return redirect('order_confirmation', order_id=order_id)
