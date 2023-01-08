import uuid
from django.contrib import admin
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html

# Create your models here

class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Product(models.Model):
    """ Product are the items which are the users primary interest in the website,
     - Product have a unique name, so they are distinguishable from each other
     """
    LABEL_TYPES = [
        ('NEW', 'N'),
        ('SALE', 'S')
    ]
    category = (
        ('Accessories', 'accessories'),('Camera', 'camera'), ('Laptop', 'laptop'), ('Audio', 'audio'),('uncategorized','Uncategorized' )
    )
    name = models.CharField(max_length=200, unique=True)
    from pyuploadcare.dj.models import ImageGroupField
    image = ImageGroupField(blank=True)
    available = models.IntegerField(default=1)
    price = models.FloatField()
    label = models.CharField(max_length=10, choices=LABEL_TYPES, default='SALE')
    description = models.TextField()
    category = models.CharField(choices=category, default='uncategorized', max_length=200)
    # colour = ArrayField(models.CharField(max_length=200,choices=LABEL_TYPES, blank=True), default=list, blank=True)
    # discount = PercentageField(blank=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.name = self.name.title()
        super().save()

    @admin.display(description="")
    def image_display(self):
        if not self.image:
            display_image = '/static/thumbnail.jpg'
        else:
            display_image = self.image[0].cdn_url
        return format_html(
            '<img src="{}" width="30">', display_image
            )
    @admin.display(description="Price")
    def price_display(self):
        return '$' +str(self.price)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """ Django's default user model is extended for this wish list option for active user,
    Shipping Address for user is saved from checkout process
    """
    wish_list = models.ManyToManyField(Product)
    city = models.CharField(max_length=20)
    mobile_number = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=200)
    zip = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.email


class OrderedItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_item')
    quantity = models.IntegerField(default=1)
    consumer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def ordered_item_total(self):
        return self.item.price * self.quantity


class Cart(models.Model):
    items = models.ManyToManyField(OrderedItem, blank=True)
    transaction_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    completed = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(blank=True, null=True)
    processing = models.BooleanField(default=False)
    consumer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def cart_total(self):
        total = sum([price.ordered_item_total() for price in self.items.all()])
        return total

    def quantity_total(self):
        return self.items.count()
