from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from store.models import Product, OrderedItem, Cart
from store.serializer import ProductInfoSerializer, UserSerializer, OrderedItemSerializer, CartSerializer


# Create your views here.

class HomeView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        response = render(request, self.template_name)
        return response


class ProductAPIView(ListAPIView):
    queryset = Product.objects.all().filter(available__lte=1)
    serializer_class = ProductInfoSerializer


@api_view(['POST', "GET"])
def api_user(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            product = Product.objects.get(id=request.data['id'])
            if product not in user.wish_list.all():
                user.wish_list.add(product)
            else:
                user.wish_list.remove(product)
    return Response(UserSerializer(user).data)


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
    return Response({'count': cart.quantity_total(), 'update':update})
