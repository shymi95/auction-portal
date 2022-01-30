from django.urls import path
from apps.cart import views

app_name = 'cart'

urlpatterns = [
    path('cart', views.Cart.as_view(), name='cart'),
    path('cart/<int:pk>', views.Item.as_view(), name='item'),
    path('cart/<int:pk>/finalize', views.Finalize.as_view(), name="finalize"),
    path('purchased', views.Purchased.as_view(), name='purchased'),
]