from rest_framework import serializers
from .models import Product, User, Cart, OrderedItem


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'price', 'image', 'label', 'id'
        ]


class OrderedItemSerializer(serializers.ModelSerializer):
    item = ProductInfoSerializer()

    class Meta:
        model = OrderedItem
        fields = [
            'item', 'quantity'
        ]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'items', 'cart_total', 'quantity_total'
        ]


class UserSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField()
    wish_list = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'wish_list', 'cart'
        ]

    def get_cart(self, obj):
        carts = Cart.objects.get(consumer=obj)
        if carts is not None:
            return CartSerializer(carts).data
        return None

    def get_wish_list(self, obj):
        return [obj.wish_list.count(), [product.id for product in obj.wish_list.all()]]
