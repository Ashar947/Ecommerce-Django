from django.contrib import admin

# Register your models here.
from .models import Category
from .models import Product , Cart , Order , user_table , Wishlist


admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(user_table)
admin.site.register(Wishlist)