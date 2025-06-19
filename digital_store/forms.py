from django import forms
from .models import Product, Category, Cart, Order, Seller, Platform, Discount, ProductType
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=2
    )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Придумайте пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'forn-control'}),
        min_length=2
    )
    password = forms.CharField(
        label='Ваш пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'photo', 'stock', 'sales_count', 'categories', 'seller', 'platforms', 'product_types']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название товара',
                'required': 'required',
                'maxlength': 255
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание товара',
                'rows': 5
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену',
                'min': 0,
                'step': '0.01',
                'required': 'required'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите количество',
                'min': 0,
                'required': 'required'
            }),
            'sales_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите количество продаж',
                'min': 0,
                'required': 'required'
            }),
            'categories': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 10,
                'required': 'required'
            }),
            'seller': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'platforms': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 3
            }),
            'product_types': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 3,
                'required': 'required'
            }),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название категории',
                'required': 'required',
                'maxlength': 255
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user']
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'total_price', 'status']
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'total_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите общую сумму',
                'min': 0,
                'step': '0.01',
                'required': 'required'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['name', 'sales_count']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название продавца',
                'required': 'required',
                'maxlength': 255
            }),
            'sales_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите количество продаж',
                'min': 0,
                'required': 'required'
            }),
        }

class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название платформы',
                'required': 'required',
                'maxlength': 255
            }),
        }

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['name', 'percentage', 'start_date', 'end_date', 'products']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название скидки',
                'required': 'required',
                'maxlength': 255
            }),
            'percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите процент скидки',
                'min': 0,
                'max': 100,
                'required': 'required'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': 'required'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': 'required'
            }),
            'products': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 100
            }),
        }

class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название типа товара',
                'required': 'required',
                'maxlength': 255
            }),
        }

