from django.urls import path, include
from cart import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_home, name="home"),
    path('update/', views.cart_update, name='update'),
]