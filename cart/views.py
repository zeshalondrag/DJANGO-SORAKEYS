from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from digital_store.models import Product, ProductType, Order, OrderItem
from .cart import Cart
from .forms import CartAddProductForm, OrderForm

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    form = CartAddProductForm(request.POST, product=product)
    if form.is_valid():
        product_type = get_object_or_404(ProductType, id=form.cleaned_data['product_type'])
        if form.cleaned_data['count'] > product.stock:
            return JsonResponse({'success': False, 'error': f"Недостаточно товара в наличии (доступно: {product.stock})."})
        cart.add(
            product=product,
            product_type=product_type,
            count=form.cleaned_data['count'],
            update_count=form.cleaned_data['reload']
        )
        return JsonResponse({'success': True, 'message': f"Товар '{product.name}' добавлен в корзину."})
    return JsonResponse({'success': False, 'error': str(form.errors)})

@require_POST
def cart_remove(request, product_id, product_type_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    product_type = get_object_or_404(ProductType, pk=product_type_id)
    cart.remove(product, product_type)
    return JsonResponse({'success': True, 'message': f"Товар '{product.name}' удалён из корзины."})

@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return JsonResponse({'success': True, 'message': "Корзина очищена."})

@require_POST
def cart_update(request, product_id, product_type_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    product_type = get_object_or_404(ProductType, pk=product_type_id)
    count = int(request.POST.get('count', 1))
    if count > product.stock:
        return JsonResponse({'success': False, 'error': f"Недостаточно товара в наличии (доступно: {product.stock})."})
    if count < 1:
        cart.remove(product, product_type)
        return JsonResponse({'success': True, 'message': f"Товар '{product.name}' удалён из корзины."})
    cart.add(product, product_type, count, update_count=True)
    return JsonResponse({'success': True, 'message': f"Количество товара '{product.name}' обновлено."})

@login_required
def cart_buy(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Ваша корзина пуста.")
        return redirect('cart:cart_detail')
    
    form = OrderForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            total_price = cart.get_total_discounted_price()
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['count'],
                    price=item['discounted_price'],
                    product_type=item['product_type']
                )
                item['product'].stock -= item['count']
                item['product'].sales_count += item['count']
                item['product'].save()

            cart.clear()
            messages.success(request, f"Заказ #{order.id} успешно оформлен!")
            return redirect('cart:order_confirmation', order_id=order.id)
    
    return render(request, 'order/order_form.html', {'form': form, 'cart': cart})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'cart/order_confirmation.html', {'order': order})