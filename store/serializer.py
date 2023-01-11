import httpx
from rest_framework import serializers
from .models import Product, User, Cart, OrderedItem, ShippingAddress


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


class CartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'products', 'cart_total', 'quantity_total'
        ]

    def get_products(self, obj):
        print(obj.items)
        data = []
        for x in obj.items.all():
            i = ProductInfoSerializer(x.item).data
            i['quantity'] = x.quantity
            data.append(i)
        return data
            
            
        

class UserSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField()
    wish_list = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'wish_list', 'cart'
        ]

    def get_cart(self, obj):
        carts, created = Cart.objects.get_or_create(consumer=obj, processing=False)
        if carts is not None:
            return CartSerializer(carts).data
        return None

    def get_wish_list(self, obj):
        return [obj.wish_list.count(), [ProductInfoSerializer(product).data for product in obj.wish_list.all()],
                sum([product.price for product in obj.wish_list.all()])]


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            'address', 'city', 'zip', 'mobile_number',
        ]
