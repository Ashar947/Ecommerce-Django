# from django.contrib import admin
from django.urls import path , include
from .import views
urlpatterns = [
    path('', views.index, name="Ecom_Home"),
    path('addtocart/<int:id>', views.addtocart, name="Ecom_AddtoCart"),
    path('category/<int:id>', views.cat, name="Ecom_Category"),
    path('cart/', views.cart, name="Ecom_Cart"),
]