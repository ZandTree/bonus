from django.urls import path
from . import views

app_name = 'shops'

urlpatterns =[
    path('',views.Home.as_view(),name='home'),
    path('products/',views.Products.as_view(),name='products'),
    path('add-product/<int:pk>/',views.AddProductToCart.as_view(),name='add-product'),
    path('cart-items/',views.ShowCartItems.as_view(),name='cart-items'),
    path('order-create/<int:pk>/',views.OrderMake.as_view(),name='order-create'),
    path('orders-list',views.ShowOrders.as_view(),name='orders-list'),
    path('bonus-cart-info/<int:pk>/',views.ShowBonusCartInfo.as_view(),name='bonuscart-info'),

]
