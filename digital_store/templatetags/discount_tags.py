from django import template
from datetime import date

register = template.Library()

@register.filter
def calculate_discounted_price(product):
    """
    Вычисляет цену товара с учётом максимальной активной скидки.
    Возвращает кортеж: (цена_со_скидкой, процент_скидки, название_скидки).
    Если скидки нет, возвращает (исходная_цена, 0, None).
    """
    discounts = product.discount_set.filter(start_date__lte=date.today(), end_date__gte=date.today())
    if not discounts.exists():
        return (float(product.price), 0, None)
    
    max_discount = max(discounts, key=lambda d: d.percentage)
    discount_percentage = max_discount.percentage
    discounted_price = float(product.price) * (1 - discount_percentage / 100)
    return (round(discounted_price, 2), discount_percentage, max_discount.name)