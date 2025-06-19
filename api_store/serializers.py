from rest_framework import serializers
from digital_store.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'photo'
        ]

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = [
            'name',
            'sales_count'
        ]

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = [
            'name'
        ]

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = [
            'name'
        ]

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(label='Цена', max_digits=10, decimal_places=2)
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'photo',
            'stock',
            'sales_count',
            'created_at',
            'categories',
            'seller',
            'platforms',
            'product_types'
        ]

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            'name',
            'percentage',
            'start_date',
            'end_date',
            'products'
        ]

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'user',
            'created_at',
            'updated_at'
        ]

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'cart',
            'product',
            'quantity',
            'product_type'
        ]

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = [
            'code',
            'discount_percentage',
            'valid_until',
            'is_active'
        ]

class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(label='Итоговая цена', max_digits=10, decimal_places=2)
    class Meta:
        model = Order
        fields = [
            'user',
            'total_price',
            'status',
            'created_at',
            'updated_at',
            'comment',
            'promo_code'
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(label='Цена', max_digits=10, decimal_places=2)
    class Meta:
        model = OrderItem
        fields = [
            'order',
            'product',
            'quantity',
            'price',
            'product_type'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'product',
            'rating',
            'price',
            'comment',
            'created_at'
        ]