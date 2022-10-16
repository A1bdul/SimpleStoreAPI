import json

from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from store.models import Product, OrderedItem, Cart
from store.serializer import ProductInfoSerializer, UserSerializer, OrderedItemSerializer


# Create your views here.

class ProductAPIView(ListAPIView):
    queryset = Product.objects.all().filter(available__lte=1)
    serializer_class = ProductInfoSerializer


@api_view(['POST', "GET"])
def api_user(request):
    user = request.user
    response = Response({'is_user': False})
    cookie = request.COOKIES.get('user-cart')
    cart = request.COOKIES.get('cookie-cart')
    if user.is_authenticated:
        response = Response(UserSerializer(user).data)
        if request.method == 'POST':
            product = Product.objects.get(id=request.data['id'])
            if product not in user.wish_list.all():
                user.wish_list.add(product)
            else:
                user.wish_list.remove(product)
        if cookie:
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
            response.delete_cookie('user-cart')
            response.delete_cookie('cookie-cart')
    else:
        if not cookie:
            response.set_cookie('user-cart', True)
    return response


@api_view(['POST'])
def api_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(consumer=user)
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


class ProductDetailTemplateView(View):
    template_name = 'product-single.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductInfoSerializer


