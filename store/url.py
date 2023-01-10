from django.urls import path

from . import views

urlpatterns = [
    path('api/product', views.ProductAPIView.as_view(), name='Product_view'),
    path('api/user', views.UserWishCartView.as_view(), name='user'),
    path('api/cart', views.CartAPIView.as_view(), name='cart'),
    path('api/checkout-point', views.CheckOutView.as_view(), name='checkout'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view()),
    path('mail/newsletter', views.NewsletterAPIView.as_view(), name="newsletter")
   ]
