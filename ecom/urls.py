# from django.contrib import admin
from django.urls import path , include
from .import views
urlpatterns = [
    path('', views.index, name="Ecom_Home"),
    path('signin/', views.user_login, name="SignIn"),
    path('handle_login/', views.handle_login, name="handle_login"),
    path('signup/', views.user_signup, name="SignUp"),
    path('logout/', views.user_logout, name="Logout"),
    path('createuser/', views.user_create, name="UserCreation"),
    path('userprofile/', views.user_profile, name="UserProfile"),
    path('editprofile/', views.viewupdateprofile, name="Update_Profile"),
    path('changepassword/', views.password, name="ChangeUserPassword"),
    path('updatepassword/', views.update_password, name="Update_Password"),
    path('UpdateProfile/', views.update_profile, name="Change_User_Profile"),
    path('addtocart/<int:id>/', views.addtocart, name="Ecom_AddtoCart"),
    path('addtowishlist/<int:id>', views.addtowishlist, name="Ecom_AddtoWishlist"),
    path('category/<int:id>/', views.cat, name="Ecom_Category"),
    path('cart/', views.cart, name="Ecom_Cart"),
    path('cart/cartdel/<int:id>', views.cartdel, name="Ecom_Cartdel"),
    path('checkout', views.checkout, name="Ecom_Checkout"),
    path('wishlist/', views.wishlist, name="Ecom_Wishlist"),
    path('search/', views.searchbar, name="Ecom_SearchBar"),
    path('orderhistory/', views.orderhistory, name="Ecom_OrderHistory"),
    path('vieworderhistory/<int:id>', views.vieworder, name="Ecom_OrderView"),
    path('decqty/<int:id>', views.decqty_cart),
    path('incqty/<int:id>', views.incqty_cart),
    path('prodpdf/<int:id>', views.prodpdf),
    # path('base', views.base, name="Ecom_Base"),
  
]