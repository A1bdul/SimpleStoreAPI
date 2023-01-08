import httpx
from rest_framework import serializers
from .models import Product, User, Cart, OrderedItem


class ProductInfoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    name = serializers.CharField()
    class Meta:
        model = Product
        fields = [
            'name', 'price', 'image', 'label', 'id', 'description', 'category'
        ]

    def get_image(self, obj):
        try:
            return [x.cdn_url for x in obj.image]
        except httpx.ConnectError:
            return ['/assets/img/product/2.jpg'] * 4


class OrderedItemSerializer(serializers.ModelSerializer):
    item = ProductInfoSerializer(read_only=True)

    class Meta:
        model = OrderedItem
        fields = [
            'item', 'quantity'
        ]


class CartSerializer(serializers.ModelSerializer):
    items = OrderedItemSerializer(many=True, read_only=True)

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
        return [obj.wish_list.count(), [ProductInfoSerializer(product).data for product in obj.wish_list.all()],
                sum([product.price for product in obj.wish_list.all()])]


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'address', 'city', 'zip', 'mobile_number', 'email'
        ]


class Check0utSerializer(serializers.Serializer):
    shipping_address = ShippingAddressSerializer()
    cart = CartSerializer()
