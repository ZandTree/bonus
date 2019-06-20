from django.shortcuts import render
from .models import Product
from django.views.generic import ListView

class Products(ListView):
    model = Product
    
