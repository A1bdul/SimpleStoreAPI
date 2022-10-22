from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_402_PAYMENT_REQUIRED, HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK
from rest_framework.views import APIView

from store.models import Product, OrderedItem, Cart, User
from store.serializer import (ProductInfoSerializer, UserSerializer, Check0utSerializer,
                              ShippingAddressSerializer
                              )


# Create your views here.


class ProductAPIView(ListAPIView):
    queryset = Product.objects.all().filter(available__gte=1)  # available items greater than or equal to 1
    serializer_class = ProductInfoSerializer  # return json format from serializer

    def post(self, request):
        # get search input from request
        search = request.data.get('s')
        # filter queryset for matching products to search
        self.queryset = Product.objects.all().filter(name__icontains=search)
        data = {}
        n = 0
        for query in self.queryset:
            serializer = ProductInfoSerializer(query)
            data[n] = serializer.data
            n += 1
        return Response(data)


class UserWishCartView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({'is_user': False})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            product = Product.objects.get(id=request.data['id'])
            if product not in user.wish_list.all():
                user.wish_list.add(product)
            else:
                user.wish_list.remove(product)


class CartAPIView(APIView):
    def get(self, request):
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
                subject, to, from_ = 'Me to the world', ['a1daromosu@gmail.com'], settings.DEFAULT_FROM_EMAIL
                message = 'Hello World'
                msg = EmailMultiAlternatives(subject, message, from_, to)
                msg.send(fail_silently=False)
                return Response({'success': 'proceed to payment'}, status=HTTP_402_PAYMENT_REQUIRED)
            else:
                return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)
