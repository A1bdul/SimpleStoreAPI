import json

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from store.models import Product, OrderedItem, Cart, User
from store.serializer import (ProductInfoSerializer, UserSerializer, OrderedItemSerializer,
                              Check0utSerializer,
                              ShippingAddressSerializer
                              )
from rest_framework.status import HTTP_402_PAYMENT_REQUIRED, HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK

# Create your views here.


class ProductAPIView(ListAPIView):
    queryset = Product.objects.all().filter(available__gte=1)  # available items greater than or equal to 1
    serializer_class = ProductInfoSerializer  # return json format from serializer


@api_view(['POST', "GET"])
def api_user(request):
    user = request.user
    response = Response({'is_user': False})
    cookie = request.COOKIES.get('user-cart')  # check whether user is active or not
    cart = request.COOKIES.get('cookie-cart')  # if user is not active, get cookie cart is set in browser
    if user.is_authenticated:
        # return user's cart and wishlist data
        response = Response(UserSerializer(user).data)

        if request.method == 'POST':
            # check if product is in user's wish list whether to add it or not.
            product = Product.objects.get(id=request.data['id'])
            if product not in user.wish_list.all():
                user.wish_list.add(product)
            else:
                user.wish_list.remove(product)
        if cookie:
            # cookie exist before user becomes active and cookie item to cart and if cart item exists in
            # database, increase item quantity
            cart = dict(json.loads(cart))
            for x in cart['item']:
                res = OrderedItemSerializer(data=x)
                if res.is_valid():
                    product = Product.objects.get(id=x['item']['id'])
                    updated, created = OrderedItem.objects.get_or_create(item=product)
                    if not created:
                        updated.quantity += x['quantity']
                    updated.quantity = x['quantity']
                print('done!!')

            # delete all cookies
            response.delete_cookie('user-cart')
            response.delete_cookie('cookie-cart')
    else:
        # if user is not active, set cookie
        if not cookie:
            response.set_cookie('user-cart', True)
    return response


@api_view(['POST'])
def api_cart(request):
    # check if product is in user's cart whether to add it or not.

    user = request.user
    cart, created = Cart.objects.get_or_create(consumer=user, processing=False)
    product = Product.objects.get(id=request.data['id'])
    updated, created = OrderedItem.objects.get_or_create(item=product)
    if updated in cart.items.filter(item=updated.item):
        cart.items.remove(updated)
        updated.delete()
        update = 'removed'
    else:
        cart.items.add(updated)
        update = 'added'
    return Response({'count': cart.quantity_total(), 'update': update})


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductInfoSerializer


class CheckOutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            request.data['cart'] = UserSerializer(request.user).data['cart']
        user = request.data['shipping_address']
        if request.data.get('payment') == 'confirmed':
            serializer = Check0utSerializer(data=request.data)
            if serializer.is_valid():
                consumer, created = User.objects.get_or_create(email=user['email'])
                cart = Cart.objects.get(consumer=consumer, processing=False)
                for x in request.data['cart']['items']:
                    product = Product.objects.get(id=x['item']['id'])
                    updated, i = OrderedItem.objects.get_or_create(item=product, consumer=consumer)
                    cart.items.add(updated)
                cart.processing = True
                cart.save()
                return Response({'success': 'cart processing started'}, status=HTTP_200_OK)
        else:
            serializer = ShippingAddressSerializer(data=user)
            if serializer.is_valid():
                return Response({'success': 'proceed to payment'}, status=HTTP_402_PAYMENT_REQUIRED)
            else:
                return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)
