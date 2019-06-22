from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .models import Product,Cart,Order
from django.views.generic import ListView,View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(TemplateView):
    template_name = 'shops/home.html'

class Products(LoginRequiredMixin,ListView):
    model = Product
    def get_queryset(self,*args,**kwargs):
        """
        just for test simplicity: user gets only prods which are
        NOT in his cart yet
        """
        cart = Cart.objects.get(user=self.request.user,accepted=False)
        prods_bought = cart.product.all().values_list('id',flat=True)
        print("all available products",Product.objects.all())
        to_see = Product.objects.exclude(id__in=prods_bought)
        return to_see


class AddProductToCart(LoginRequiredMixin,View):
    def get(self,request,pk):
        prod = get_object_or_404(Product,id=pk)
        cart = Cart.objects.get(user=request.user,accepted=False)
        all_prods = cart.product.all()
        cart.product.add(prod)
        cart.save()
        return redirect('/')
        # return redirect('shops:product-list')

class ShowCartItems(LoginRequiredMixin,ListView):
    """
    show items added to cart
    """
    template_name = 'shops/cart_items.html'
    context_object_name = 'products'
    model = Product

    def get_queryset(self,*args,**kwargs):
        cart = Cart.objects.get(user=self.request.user,accepted=False)
        return cart.product.all()

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart.objects.get(user=self.request.user,accepted=False)
        return context

class OrderMake(LoginRequiredMixin,View):
    def get(self,request,pk):
        cart = get_object_or_404(Cart,id=pk,accepted=False)
        order = Order.objects.create(cart=cart)
        print('order created',order)
        cart.accepted = True
        cart.save()
        new_cart = Cart.objects.create(user=request.user,accepted=False)
        return redirect ("shops:orders-list")

class ShowOrders(LoginRequiredMixin,ListView):
    model = Order
    def get_queryset(self):
        return Order.objects.filter(cart__user = self.request.user)
