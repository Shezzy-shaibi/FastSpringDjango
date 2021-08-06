from django.db import models


class Create_subscription(models.Model):
    product_ref = models.CharField(max_length=200, null=True, blank=True, verbose_name="Product Reference")
    interval = models.CharField(max_length=200,null=True, blank=True, verbose_name="Subscription interval")
    trial = models.CharField(max_length=200, null=True, blank=True, verbose_name="Trial")
    price = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)
    date = models.DateTimeField(verbose_name="Creation Date", auto_now=True)





class Product(models.Model):
    STATUS = [
        (True, 'Published'),
        (False, 'Draft'),
    ]

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, verbose_name="Product Path")
    description = models.TextField()
    img = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Image")

    price = models.DecimalField(decimal_places=2, max_digits=100)
    trial = models.CharField(max_length=10,null=True,blank=True)
    subscription_interval = models.CharField(max_length=100, null=True, blank=True,verbose_name="Subscription interval")
    date = models.DateTimeField(verbose_name="Creation Date", auto_now=True)

    def __str__(self):
        return self.name
# Create your models name.
