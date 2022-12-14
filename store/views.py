from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_402_PAYMENT_REQUIRED, HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK
from rest_framework.views import APIView
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import os 
from store.models import Product, OrderedItem, Cart, User, Newsletter
from store.serializer import (ProductInfoSerializer, UserSerializer,
                ShippingAddressSerializer)
import threading
from dotenv import load_dotenv
from django.db.models import Q
load_dotenv()
# Create your views here.

class EmailThread(threading.Thread):
    
    def __init__(self, subject, email,  msg):
        self.subject = subject
        self.msg = msg
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        print("sent!!")
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = str(os.getenv('SENDINBLUE_API_KEY'))
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        # Define the campaign settings\
        email_campaigns = sib_api_v3_sdk.SendSmtpEmail(
        subject= self.subject,
        sender= { "name": "Israel", "email": self.email},
        to = [{'email': settings.DEFAULT_TO_EMAIL, "name":"Abdul"}],
        # Content that will be sent\
        html_content= self.msg,
        )
        # Make the call to the client\
        try:
            api_response = api_instance.send_transac_email(email_campaigns)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling EmailCampaignsApi->create_email_campaign: %s\n" % e)# ------------------
        # Include the Sendinblue library\



class ProductAPIView(ListAPIView):
    queryset = Product.objects.all().filter(available__gte=1)  # available items greater than or equal to 1
    serializer_class = ProductInfoSerializer  # return json format from serializer

    def post(self, request):
        # get search input from request
        search = request.data.get('s')
        range = request.data.get('range')
        print(range, search)
        # filter queryset for matching products to search
        self.queryset = Product.objects.all().filter(Q(Q(category__icontains=search.replace('&amp;', '&')) & Q(price__range=(range[1], range[0]))) | Q(name__icontains=search))
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
    """
        data =  
        { 
            shipping_address: {
                firstname: firstname,
                lastname: lastname,
                email: email,
                mobile_number: mobile_number,
                zip: zip,
                city: city,
                country: country,
                state:state,
                address: address
            },
            cart: {
                products:[{
                            "name": "Laced Jacket With Strips",
                            "id": 2,
                            "quantity": 3
                        },{
                            "name": "Baggy Jacket With Pockets",
                            "id": 1,
                            "quantity": 1
                        }]
                }
            }
    """
    def post(self, request):
        if request.user.is_authenticated:
            # get authenticated user's cart from database
            request.data['cart'] = UserSerializer(request.user).data['cart']
        user = request.data['shipping_address']
        if request.data.get('payment') == 'confirmed':
            consumer, created = User.objects.get_or_create(email=user['email'])
            cart = Cart.objects.get(consumer=consumer, processing=False)
            for x in request.data['cart']['items']:
                product = Product.objects.get(id=x['id'])
                updated, i = OrderedItem.objects.get_or_create(item=product, consumer=consumer, quantity=x['quantity'])
                cart.items.add(updated)
            cart.processing = True
            cart.save()
            subject, to, from_ = 'Me to the world', ['a1daromosu@gmail.com'], settings.DEFAULT_FROM_EMAIL
            message = 'Hello World'
            EmailThread(subject, consumer.email, message).start()
            return Response({'success': 'cart processing started'}, status=HTTP_200_OK)
        else:
            serializer = ShippingAddressSerializer(data=user)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': 'proceed to payment'}, status=HTTP_402_PAYMENT_REQUIRED)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=HTTP_406_NOT_ACCEPTABLE)


class NewsletterAPIView(APIView):
    def post(self, request):
        subject = 'Me to the World'
        email = request.data.get('email')
        msg = 'YOur email is Successfully added to Our Newsletter'
        EmailThread(subject, email, msg).start()
        Newsletter.objects.create(email=email)
        return Response("Email succesfully added to neswletter")
    
    