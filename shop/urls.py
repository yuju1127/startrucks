from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('cakes/',views.cakes, name='cakes'),
    path('trappuccino/',views.trap, name='trap'),
    path('coffee/',views.coffee, name='coffee'),
    path('sandwich/',views.sand, name='sand'),
    path('register/',views.register,name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('order_cakes/<int:cakes_id>', views.order_cakes, name='order_cakes'),
    path('order_coffee/<int:coffees_id>', views.order_coffee, name='order_coffee'),
    path('order_sandwiches/<int:sandwiches_id>', views.order_sandwich, name='order_sandwich'),
    path('order_trappuccinos/<int:trappuccinos_id>', views.order_trappuccino, name='order_trappuccino'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('order_history/', views.order_history, name='order_history'),
    path('order_increase/<int:cart_item_id>/', views.order_increase, name='order_increase'),
    path('order_decrease/<int:cart_item_id>/', views.order_decrease, name='order_decrease'),
    path('order_delete/<int:cart_item_id>/', views.order_delete, name='order_delete'),
    path('order_confirm/<int:cart_item_id>/', views.order_confirm, name='order_confirm'),
    path('add_item_to_order/<int:order_id>/', views.add_item_to_order, name='add_item_to_order'),

]