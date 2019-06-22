from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from utils import make_avatar



STATUS = (
    ('cl','client'),
    ('ad','admin'),
    ('as','shop_assiant')

)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    status = models.CharField(max_length=2,choices=STATUS,default='cl')
    created = models.DateTimeField(auto_now_add=True)
    postcode = models.CharField(max_length=24,default="")
    state = models.CharField(max_length=124,default="")
    city = models.CharField(max_length=124,default="")
    avatar = models.ImageField(blank=True,null=True,upload_to=make_avatar)


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profiles:profile',kwargs={'pk':self.id})
    @property
    def get_ava_path(self,*args,**kwargs):
        if self.avatar:
            return '/media/{}'.format(self.avatar)
        else:
            return '/static/img/day.jpg/'

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height >200 or img.width >200:
                output_size = (200,200)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

#
# def created_profile(sender,instance,created,*args,**kwargs):
#     if created and instance.email:
#         print('creating a profile for this user')
#         Profile.objects.get_or_create(user=instance,email=instance.email)
# post_save.connect(created_profile,sender=User)

@receiver(post_save,sender = User)
def create_user_profile(sender,instance,created,**kwargs):
    """As New User created, create Profile"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    """As New User created, save Profile"""
    instance.profile.save()
