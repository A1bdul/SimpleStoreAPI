import uuid

from django import forms
from django.core import exceptions
from django.db import models
from django.contrib.auth.models import AbstractUser
from pyuploadcare.dj.models import ImageGroupField
# from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _


# Create your models here
# class PercentageField(models.CharField):
#     empty_values = True
#     description = _('Returns percentage format for string')
#
#     def __init__(self, *args, **kwargs):
#         max_length = 200
#         super(PercentageField, self).__init__(max_length, *args, **kwargs)
#
#     def to_python(self, value):
#         if value is None:
#             return value
#         else:
#             try:
#                 return str(float(value) / 100) + '%'
#             except (ValueError, TypeError):
#                 raise exceptions.ValidationError(
#                     self.error_messages['invalid'],
#                     code='invalid',
#                     params={'value': value}
#                 )


class Product(models.Model):
    LABEL_TYPES = [
        ('N', 'NEW'),
        ('S', 'SALE')
    ]

    name = models.CharField(max_length=200)
    image = ImageGroupField(blank=True)
    available = models.IntegerField(default=1)
    price = models.FloatField()
    label = models.CharField(max_length=10, choices=LABEL_TYPES, default='SALE')

    # discount = PercentageField(blank=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.name = self.name.title()
        super().save()

    def __str__(self):
        return self.name


class OrderedItem(models.Model):
    item = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='ordered_item')
    quantity = models.IntegerField(default=1)

    def ordered_item_total(self):
        return self.item.price * self.quantity


class User(AbstractUser):
    wish_list = models.ManyToManyField(Product)


class Cart(models.Model):
    transaction_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    consumer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    items = models.ManyToManyField(OrderedItem)
    completed = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def cart_total(self):
        total = sum([price.ordered_item_total() for price in self.items.all()])
        return total

    def quantity_total(self):
        return self.items.count()
