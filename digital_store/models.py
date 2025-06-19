from django.db import models
from django.contrib.auth.models import User
from datetime import date
from decimal import Decimal

MAX_LENGTH = 255

class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название категории')
    photo = models.ImageField(upload_to='static/images/categories/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Seller(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название продавца')
    sales_count = models.PositiveIntegerField(default=0, verbose_name='Количество продаж')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

class Platform(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название платформы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Платформа'
        verbose_name_plural = 'Платформы'

class ProductType(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название типа товара')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'

class Product(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название игры')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    photo = models.ImageField(upload_to='static/images/products/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')
    stock = models.PositiveIntegerField(default=0, verbose_name='Количество в наличии')
    sales_count = models.PositiveIntegerField(default=0, verbose_name='Количество продаж')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    categories = models.ManyToManyField(Category, verbose_name='Категории')
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, verbose_name='Продавец')
    platforms = models.ManyToManyField(Platform, verbose_name='Платформы')
    product_types = models.ManyToManyField(ProductType, verbose_name='Типы товара')

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"

    def get_discounted_price(self):
        active_discount = self.discount_set.filter(
            start_date__lte=date.today(),
            end_date__gte=date.today()
        ).first()
        if active_discount:
            return self.price * (Decimal(1) - Decimal(active_discount.percentage) / Decimal(100))
        return self.price

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Discount(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название скидки')
    percentage = models.PositiveIntegerField(verbose_name='Процент скидки')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    products = models.ManyToManyField(Product, blank=True, verbose_name='Товары')

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

    def is_active(self):
        today = date.today()
        return self.start_date <= today <= self.end_date

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"Корзина {self.user.username}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, verbose_name='Тип товара')

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Код')
    discount_percentage = models.PositiveIntegerField(verbose_name='Процент скидки')
    valid_until = models.DateField(verbose_name='Действителен до')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}%)"

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Ожидает'),
        ('Processing', 'В обработке'),
        ('Shipped', 'Отправлен'),
        ('Delivered', 'Доставлен'),
        ('Cancelled', 'Отменен'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')
    promo_code = models.ForeignKey(PromoCode, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Промокод')

    def __str__(self):
        return f"Заказ #{self.id} ({self.user.username})"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, verbose_name='Тип товара')

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, verbose_name='Оценка')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Отзыв на {self.product.name} ({self.rating})"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'