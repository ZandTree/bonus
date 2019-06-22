from django.db import models
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
        summa = self.cart.get_total()
        discount_price= summa - (summa/100*self.discount)
        # return format(discount_price,".2f")
        return discount_price

# time = datetime(2010, 6, 21, 19, 31, 50, 894934)
# time_2 = datetime(2019, 6, 22, 12, 0, 24, 423780, tzinfo=<UTC>)
STATUS = (
    ('valid','valid'),
    ('invalid','invalid')
)
class BonusCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='bonus',blank=True,null=True)
    uid = models.CharField(max_length=4,blank=True,null=True)
    valid = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    last_used = models.DateTimeField(auto_now=True,blank=True,null=True)
    status = models.CharField(max_length=7,choices=STATUS,default='valid')
    summ_total = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    expired = models.DateTimeField()

# option N1
"""
при создании юзера создаю бонусную карту с отсут-им unid,
далее вызываю сигнал (pre_save for BonusCart) и добавляю uid,после чего сохраняю
object BonusCart
"""
"""
@receiver(post_save,sender = User)
def create_bounuscart(sender,instance,created,**kwargs):
    #As New User created, create BonusCart
    if created:
        created = timezone.now()
        expired = timezone.now() + timedelta(days=180)
        bonus= BonusCart.objects.get_or_create(user=instance,created_at=created,expired=expired)

def bonuscart_presave_receiver(sender, instance,*args,**kwargs):
    if not instance.uid: # if already created => no need to change
        instance.uid = create_uid(instance)
        # don't call here save(!)
pre_save.connect(bonuscart_presave_receiver,sender=BonusCart)
"""

# option N2 (очень старнный,но всё в одном под присмотром)
def create_bonus(sender, instance,created,*args,**kwargs):
    """As New User created, create BonusCart """
    if created:
        created = timezone.now()
        expired = timezone.now() + timedelta(days=180)
        while True:
            uid = rand_string(5)
            print(uid)
            if BonusCart.objects.filter(uid=uid).exists():
                continue
            else:
                break
        BonusCart.objects.get_or_create(user=instance,created_at=created,expired=expired,uid=uid)
post_save.connect(create_bonus,sender=User)

# Option N3 (with error, хотя бонусная карта успешно создаётся вместе с юзером)
"""
почему в этой строке кода возикает ошибка: AttributeError: 'RelatedManager' object has no attribute 'save', а в при создании объекта Профиля(см ниже),сопряжённого с созданием юзера,
этой ошибки не возникает и метод находится?
line:104 ==> instance.bonus.save()
"""

# создание бонусной карты,сопряжённой с созданием юзера
# отношение: User,BonusCart ==> oneToMany
# @receiver(post_save,sender = User)
# def create_user_profile(sender,instance,created,**kwargs):
#     """As New User created, create BonusCart """
#     if created:
#         created = timezone.now()
#         expired = timezone.now() + timedelta(days=180)
#         bonus= BonusCart.objects.get_or_create(user=instance,created_at=created,expired=expired)
# def bonuscart_presave_receiver(sender, instance,*args,**kwargs):
#     if not instance.uid: # if already created => no need to change
#         instance.uid = create_uid(instance)
#         
# pre_save.connect(bonuscart_presave_receiver,sender=BonusCart)
# @receiver(post_save,sender=User)
# def save_user_bonuscart(sender,instance,**kwargs):
#     """As New User created, save BonusCart"""
#     instance.bonus.save() #ОШИБКА

# создание профиля,сопряжённой с созданием юзера
# отношение:User Profile ==> oneToOne
# @receiver(post_save,sender = User)
# def create_user_profile(sender,instance,created,**kwargs):
#     """As New User created, create Profile"""
#     if created:
#         Profile.objects.create(user=instance)#
# @receiver(post_save,sender=User)
# def save_user_profile(sender,instance,**kwargs):
#     """As New User created, save Profile"""
#     instance.profile.save() # No ERROR
