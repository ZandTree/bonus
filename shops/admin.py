from django.contrib import admin
from .models import Product,Cart,Order,BonusCart

admin.site.register(Order)
admin.site.register(BonusCart)
admin.site.register(Product)
admin.site.register(Cart)
# Register your models here.
