from django.shortcuts import render
from .serializers import *
from .permission import *
from rest_framework import viewsets, mixins
from digital_store.models import *

class CategoryViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomPermission]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Category.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

class SellerViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [CustomPermission]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Seller.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

class PlatformViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [CustomPermission]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Platform.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

class ProductTypeViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [CustomPermission]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = ProductType.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

class ProductViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CustomPermission]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Product.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

class DiscountViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [CustomPermission]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Discount.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

class CartViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  # mixins.CreateModelMixin,
                  # mixins.UpdateModelMixin,
                  # mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [CustomPermission]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Cart.objects.all()
        user = self.request.query_params.get('user', None)

        if user is not None:
            queryset = queryset.filter(name__icontains=user)

        return queryset

class CartItemViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  # mixins.CreateModelMixin,
                  # mixins.UpdateModelMixin,
                  # mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [CustomPermission]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = CartItem.objects.all()
        cart = self.request.query_params.get('cart', None)

        if cart is not None:
            queryset = queryset.filter(name__icontains=cart)

        return queryset

class PromoCodeViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = [CustomPermission]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = PromoCode.objects.all()
        code = self.request.query_params.get('code', None)

        if code is not None:
            queryset = queryset.filter(name__icontains=code)

        return queryset

class OrderViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CustomPermission]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Order.objects.all()
        user = self.request.query_params.get('user', None)

        if user is not None:
            queryset = queryset.filter(name__icontains=user)

        return queryset

class OrderItemViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  # mixins.CreateModelMixin,
                  # mixins.UpdateModelMixin,
                  # mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [CustomPermission]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = OrderItem.objects.all()
        order = self.request.query_params.get('order', None)

        if order is not None:
            queryset = queryset.filter(name__icontains=order)

        return queryset

class ReviewViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  # mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CustomPermission]
    pagination_class = PaginationPage

    def get_queryset(self):
        queryset = Review.objects.all()
        user = self.request.query_params.get('user', None)

        if user is not None:
            queryset = queryset.filter(name__icontains=user)

        return queryset