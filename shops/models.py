from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Product(models.Model):
    name = models.CharField(max_length=124)
    price = models.DecimalField(default = 1,max_digits=5,decimal_places=2)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User,related_name='carts',on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    product = models.ManyToManyField(Product,related_name='products_carts',blank=True)

    def __str__(self):
        return 'cart id:{} belongs to {}'.format(self.id,self.user)

def create_cart(sender,instance,created,*args,**kwargs):
    if created:
        Cart.objects.get_or_create(user=instance)        
post_save.connect(create_cart,sender=User)
