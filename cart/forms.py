from datetime import timezone
from django import forms
from digital_store.models import Order, PromoCode

class CartAddProductForm(forms.Form):
    count = forms.IntegerField(
        min_value=1,
        initial=1,
        label='Количество',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    product_type = forms.ChoiceField(
        label='Тип товара',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    reload = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        if product:
            self.fields['product_type'].choices = [
                (pt.id, pt.name) for pt in product.product_types.all()
            ]

class OrderForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@domain.com'})
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'})
    )
    payment_method = forms.ChoiceField(
        label='Способ оплаты',
        choices=[
            ('card', 'Карта (Visa/MasterCard/Mir)'),
            ('paypal', 'PayPal'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    promo_code = forms.CharField(
        label='Промокод',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите промокод'})
    )
    agree_terms = forms.BooleanField(
        label='Я согласен с правилами покупки',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Order
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваши пожелания к заказу',
                'rows': 4
            }),
        }

    def clean_promo_code(self):
        promo_code = self.cleaned_data.get('promo_code')
        if promo_code:
            try:
                promo = PromoCode.objects.get(
                    code=promo_code,
                    is_active=True,
                    valid_until__gte=timezone.now().date()
                )
                return promo
            except PromoCode.DoesNotExist:
                raise forms.ValidationError("Недействительный или истёкший промокод.")
        return None

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email