from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('api/product', views.ProductAPIView.as_view(), name='Product_view'),
    path('api/user', views.api_user, name='user'),
    path('api/cart', views.api_cart, name='cart'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view()),
    path('product/<int:pk>', views.ProductDetailTemplateView.as_view())
]
