from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime,timedelta
from utils import create_uid,rand_string
from django.dispatch import receiver

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

    def get_total(self):
        total = self.product.all().aggregate(total_price=Sum('price'))
        return total.get('total_price')

def create_cart(sender,instance,created,*args,**kwargs):
    """ As new User created,create cart """
    if created:
        Cart.objects.get_or_create(user=instance)
post_save.connect(create_cart,sender=User)

class Order(models.Model):
    status = models.BooleanField(default=False)
    cart = models.ForeignKey(Cart,related_name='order',on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(default=0,max_digits=3,decimal_places=2)

    def __str__(self):
        return 'Order No {}'.format(self.id)

    def get_total(self):
        """ return sum to pay inclusive discount in decimal format """
        summa = self.cart.get_total()
        discount_price= summa - (summa/100*self.discount)
        # return format(discount_price,".2f")
        return discount_price


class BonusCartManager(models.Manager):
    def get_valid_bonuscart(self,*args,**kwargs):
        return super().all(*args,**kwargs).filter(valid=True)
# time = datetime(2010, 6, 21, 19, 31, 50, 894934)
# time_2 = datetime(2019, 6, 22, 12, 0, 24, 423780, tzinfo=<UTC>)

STATUS = (
    ('valid','valid'),
    ('invalid','invalid')
)
class BonusCart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='bonus',blank=True,null=True)
    uid = models.CharField(max_length=4,blank=True,null=True)
    valid = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    last_used = models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=7,choices=STATUS,default='valid')
    summ_total = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    expired = models.DateTimeField()

    objects = BonusCartManager()
    def save(self,*args,**kwargs):
        current_date_time = timezone.now()
        if current_date_time > self.expired:
            print('check for validity')
            self.status = 'invalid'
        super().save(*args,**kwargs)
    def __str__(self):
        return "bonus-cart N {}".format(self.uid)
    def get_absolute_url(self):
        return reverse('shops:bonuscart',kwargs={'pk':self.id})

@receiver(post_save,sender = User)
def create_bounuscart(sender,instance,created,**kwargs):
    #As New User created, create BonusCart
    if created:
        created = timezone.now()
        expired = timezone.now() + timedelta(days=180)
        print(expired)
        bonus= BonusCart.objects.get_or_create(user=instance,created_at=created,expired=expired)
        # don't use here .save()!

def bonuscart_presave_receiver(sender, instance,*args,**kwargs):
    if not instance.uid: # if already created => no need to change
        instance.uid = create_uid(instance)
        # don't call here save(!)
pre_save.connect(bonuscart_presave_receiver,sender=BonusCart)

# AttributeError: 'RelatedManager' object has no attribute 'save',
#line:104 ==> instance.bonus.save()
