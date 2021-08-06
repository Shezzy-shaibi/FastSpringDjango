from django.contrib import admin

from .models import Product, Create_subscription
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['slug','price','subscription_interval','date']

@admin.register(Create_subscription)
class Create_subscriptionAdmin(admin.ModelAdmin):
    list_display = ['product_ref','interval','trial','price','date']

