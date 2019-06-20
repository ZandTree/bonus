from django.urls import path
from . import views

app_name = 'shops'

urlpatterns =[
    path('',views.Home.as_view(),name='home'),
    path('products/',views.Products.as_view(),name='products'),
    path('add-product/<int:pk>/',views.AddProductToCart.as_view(),name='add-product'),
]
