from django.urls import path
from . import views

app_name = 'shops'

urlpatterns =[
    path('',views.Products.as_view(),name='products'),
]
