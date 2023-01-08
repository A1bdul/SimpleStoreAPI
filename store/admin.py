from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_display', 'name', 'price_display']
    list_filter = ['category',]
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderedItem)
admin.site.register(Cart)
admin.site.register(User)
