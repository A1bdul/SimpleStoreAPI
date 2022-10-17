from django.urls import path

from . import views

urlpatterns = [
    path('api/product', views.ProductAPIView.as_view(), name='Product_view'),
    path('api/user', views.api_user, name='user'),
    path('api/cart', views.api_cart, name='cart'),
    path('api/checkout-point', views.CheckOutView.as_view(), name='checkout'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view()),
   ]
