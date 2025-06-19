from .views import *
from rest_framework import routers

urlpatterns = [
    
]

router = routers.SimpleRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('seller', SellerViewSet, basename='seller')
router.register('platform', PlatformViewSet, basename='platform')
router.register('product-type', ProductTypeViewSet, basename='product-type')
router.register('product', ProductViewSet, basename='product')
router.register('discount', DiscountViewSet, basename='discount')
router.register('cart', CartViewSet, basename='cart')
router.register('cart-item', CartItemViewSet, basename='cart-item')
router.register('promocode', PromoCodeViewSet, basename='promocode')
router.register('order', OrderViewSet, basename='order')
router.register('order-item', OrderItemViewSet, basename='order-item')
router.register('review', ReviewViewSet, basename='review')
urlpatterns += router.urls