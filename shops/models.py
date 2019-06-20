from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=124)
    price = models.DecimalField(default = 1,max_digits=5,decimal_places=2)

    def __str__(self):
        return self.name

         
