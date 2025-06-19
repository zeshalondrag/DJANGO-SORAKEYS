from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .models import *
from .forms import *
from cart.forms import CartAddProductForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home_view')
    return render(request, 'auth/login.html')

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('home_view')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', context={'form': form})

def registration_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('home_view')
    else:
        form = RegistrationForm()
    return render(request, 'auth/registration.html', context={'form': form})

def logout_user(request):
    logout(request)
    return redirect('home_view')

def home_view(request):
    discounted_products = Product.objects.filter(
        discount__start_date__lte=timezone.now(),
        discount__end_date__gte=timezone.now()
    ).distinct()[:4]

    popular_products = Product.objects.order_by('-sales_count')[:4]

    context = {
        'discounted_products': discounted_products,
        'popular_products': popular_products,
    }
    return render(request, 'pages/home.html', context)

def catalog_view(request):
    products = Product.objects.all()
    
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query))
    
    price_min = request.GET.get('price_min')
    if price_min:
        products = products.filter(price__gte=price_min)
    
    price_max = request.GET.get('price_max')
    if price_max:
        products = products.filter(price__lte=price_max)
    
    platform_id = request.GET.get('platform')
    if platform_id:
        products = products.filter(platforms__id=platform_id)
    
    genre_id = request.GET.get('genre')
    if genre_id:
        products = products.filter(categories__id=genre_id)
    
    if request.GET.get('on_sale'):
        products = products.filter(discount__start_date__lte=datetime.date.today(), discount__end_date__gte=datetime.date.today())
    
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'popular':
        products = products.order_by('-sales_count')
    
    paginator = Paginator(products, 6)  
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'products': products_page,
        'platforms': Platform.objects.all(),
        'genres': Category.objects.all(),
    }
    return render(request, 'pages/catalog.html', context)

def detail_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'pages/detail_product.html', context)

class CartView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'pages/cart.html'
    context_object_name = 'carts'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

def about_view(request):
    return render(request, 'pages/about.html')

def contacts_view(request):
    return render(request, 'pages/contacts.html')

def find_us_view(request):
    return render(request, 'pages/find_us.html')

class AdminPanelView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'digital_store.view_admin_panel'
    template_name = 'admin_panel/admin_panel.html'
    model = Product  
    context_object_name = 'products'

class ProductListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'digital_store.view_product'
    model = Product
    template_name = 'admin_panel/products/product_list.html'
    context_object_name = 'products'

class ProductDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'digital_store.view_product'
    model = Product
    template_name = 'admin_panel/products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_cart'] = CartAddProductForm()
        return context

class ProductCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'digital_store.add_product'
    model = Product
    form_class = ProductForm
    template_name = 'admin_panel/products/product_form.html'
    success_url = reverse_lazy('product_list_view')

class ProductUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'digital_store.change_product'
    model = Product
    form_class = ProductForm
    template_name = 'admin_panel/products/product_form.html'
    success_url = reverse_lazy('product_list_view')

class ProductDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'digital_store.delete_product'
    model = Product
    template_name = 'admin_panel/products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list_view')

class CategoryListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'digital_store.view_category'
    model = Category
    template_name = 'admin_panel/categories/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'digital_store.view_category'
    model = Category
    template_name = 'admin_panel/categories/category_detail.html'
    context_object_name = 'category'

class CategoryCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'digital_store.add_category'
    model = Category
    form_class = CategoryForm
    template_name = 'admin_panel/categories/category_form.html'
    success_url = reverse_lazy('category_list_view')

class CategoryUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'digital_store.change_category'
    model = Category
    form_class = CategoryForm
    template_name = 'admin_panel/categories/category_form.html'
    success_url = reverse_lazy('category_list_view')

class CategoryDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'digital_store.delete_category'
    model = Category
    template_name = 'admin_panel/categories/category_confirm_delete.html'
    success_url = reverse_lazy('category_list_view')

class CartListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'digital_store.view_cart'
    model = Cart
    template_name = 'admin_panel/carts/cart_list.html'
    context_object_name = 'carts'

class CartDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'digital_store.view_cart'
    model = Cart
    template_name = 'admin_panel/carts/cart_detail.html'
    context_object_name = 'cart'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = self.object.cartitem_set.all()
        return context

class CartCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'digital_store.add_cart'
    model = Cart
    form_class = CartForm
    template_name = 'admin_panel/carts/cart_form.html'
    success_url = reverse_lazy('cart_list_view')

class CartUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'digital_store.change_cart'
    model = Cart
    form_class = CartForm
    template_name = 'admin_panel/carts/cart_form.html'
    success_url = reverse_lazy('cart_list_view')

class CartDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'digital_store.delete_cart'
    model = Cart
    template_name = 'admin_panel/carts/cart_confirm_delete.html'
    success_url = reverse_lazy('cart_list_view')

class OrderListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'digital_store.view_order'
    model = Order
    template_name = 'admin_panel/orders/order_list.html'
    context_object_name = 'orders'

class OrderDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'digital_store.view_order'
    model = Order
    template_name = 'admin_panel/orders/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.orderitem_set.all()
        return context

class OrderCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'digital_store.add_order'
    model = Order
    form_class = OrderForm
    template_name = 'admin_panel/orders/order_form.html'
    success_url = reverse_lazy('order_list_view')

class OrderUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'digital_store.change_order'
    model = Order
    form_class = OrderForm
    template_name = 'admin_panel/orders/order_form.html'
    success_url = reverse_lazy('order_list_view')

class OrderDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'digital_store.delete_order'
    model = Order
    template_name = 'admin_panel/orders/order_confirm_delete.html'
    success_url = reverse_lazy('order_list_view')

class SellerListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'digital_store.view_seller'
    model = Seller
    template_name = 'admin_panel/sellers/seller_list.html'
    context_object_name = 'sellers'

class SellerDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'digital_store.view_seller'
    model = Seller
    template_name = 'admin_panel/sellers/seller_detail.html'
    context_object_name = 'seller'

class SellerCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'digital_store.add_seller'
    model = Seller
    form_class = SellerForm
    template_name = 'admin_panel/sellers/seller_form.html'
    success_url = reverse_lazy('seller_list_view')

class SellerUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'digital_store.change_seller'
    model = Seller
    form_class = SellerForm
    template_name = 'admin_panel/sellers/seller_form.html'
    success_url = reverse_lazy('seller_list_view')

class SellerDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'digital_store.delete_seller'
    model = Seller
    template_name = 'admin_panel/sellers/seller_confirm_delete.html'
    success_url = reverse_lazy('seller_list_view')

class PlatformListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'digital_store.view_platform'
    model = Platform
    template_name = 'admin_panel/platforms/platform_list.html'
    context_object_name = 'platforms'

class PlatformDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'digital_store.view_platform'
    model = Platform
    template_name = 'admin_panel/platforms/platform_detail.html'
    context_object_name = 'platform'

class PlatformCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'digital_store.add_platform'
    model = Platform
    form_class = PlatformForm
    template_name = 'admin_panel/platforms/platform_form.html'
    success_url = reverse_lazy('platform_list_view')

class PlatformUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'digital_store.change_platform'
    model = Platform
    form_class = PlatformForm
    template_name = 'admin_panel/platforms/platform_form.html'
    success_url = reverse_lazy('platform_list_view')

class PlatformDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'digital_store.delete_platform'
    model = Platform
    template_name = 'admin_panel/platforms/platform_confirm_delete.html'
    success_url = reverse_lazy('platform_list_view')

class DiscountListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'digital_store.view_discount'
    model = Discount
    template_name = 'admin_panel/discounts/discount_list.html'
    context_object_name = 'discounts'

class DiscountDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'digital_store.view_discount'
    model = Discount
    template_name = 'admin_panel/discounts/discount_detail.html'
    context_object_name = 'discount'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.products.all()
        return context

class DiscountCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'digital_store.add_discount'
    model = Discount
    form_class = DiscountForm
    template_name = 'admin_panel/discounts/discount_form.html'
    success_url = reverse_lazy('discount_list_view')

class DiscountUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'digital_store.change_discount'
    model = Discount
    form_class = DiscountForm
    template_name = 'admin_panel/discounts/discount_form.html'
    success_url = reverse_lazy('discount_list_view')

class DiscountDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'digital_store.delete_discount'
    model = Discount
    template_name = 'admin_panel/discounts/discount_confirm_delete.html'
    success_url = reverse_lazy('discount_list_view')

class ProductTypeListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'digital_store.view_producttype'
    model = ProductType
    template_name = 'admin_panel/product_types/product_type_list.html'
    context_object_name = 'product_types'

class ProductTypeDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'digital_store.view_producttype'
    model = ProductType
    template_name = 'admin_panel/product_types/product_type_detail.html'
    context_object_name = 'product_type'

class ProductTypeCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'digital_store.add_producttype'
    model = ProductType
    form_class = ProductTypeForm
    template_name = 'admin_panel/product_types/product_type_form.html'
    success_url = reverse_lazy('product_type_list_view')

class ProductTypeUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'digital_store.change_producttype'
    model = ProductType
    form_class = ProductTypeForm
    template_name = 'admin_panel/product_types/product_type_form.html'
    success_url = reverse_lazy('product_type_list_view')

class ProductTypeDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'digital_store.delete_producttype'
    model = ProductType
    template_name = 'admin_panel/product_types/product_type_confirm_delete.html'
    success_url = reverse_lazy('product_type_list_view')