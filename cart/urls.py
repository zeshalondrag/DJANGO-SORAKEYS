from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/<int:product_type_id>/', cart_remove, name='cart_remove'),
    path('clear/', cart_clear, name='cart_clear'),
    path('buy/', cart_buy, name='cart_buy'),
    path('order-confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('update/<int:product_id>/<int:product_type_id>/', cart_update, name='cart_update'),
]