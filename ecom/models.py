from django.db import models
from django.contrib.auth.models import User
import ast
# user : Ashar Pass:123

class Category(models.Model):
    category_name=models.CharField(max_length=25,default="")
    category_image = models.ImageField(upload_to='ecom/images',default="")
    def __str__(self):
        return self.category_name
    


class user_table(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    country = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    contact_number=models.IntegerField()
    profile_image=models.ImageField(upload_to='user/images',default='user/images/default.PNG')

    def __str__(self):
        return self.user.username #first_name


   

class Product(models.Model):
    Name = models.CharField(max_length=25)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)        
    Price = models.IntegerField(default=0)
    Description = models.CharField(max_length=100)
    Publish_Date = models.DateField()
    Image = models.ImageField(upload_to='ecom/images')
    def __str__(self):
        return self.Name
    


class Cart(models.Model):
    User = models.CharField(max_length=150)
    prod_id = models.IntegerField()
    Name_Cart = models.CharField(max_length=25)
    Category_Cart = models.ForeignKey(Category, on_delete=models.CASCADE)        
    Price_Cart = models.IntegerField()
    Quantity = models.IntegerField()
    sum = models.IntegerField()
    Image_Cart = models.ImageField(upload_to='ecom/images')
    def __str__(self):
        return self.Name_Cart  
    
    @property
    def sumtotal(self):
        total = self.Quantity * self.Price_Cart
        return total
class Wishlist(models.Model):
    user = models.CharField(max_length=150)
    Name = models.CharField(max_length=25)
    Category= models.ForeignKey(Category, on_delete=models.CASCADE)        
    Price= models.IntegerField()
    Image = models.ImageField(upload_to='ecom/images')
    def __str__(self):
        return self.Name

class Order(models.Model):
    user = models.CharField(max_length=150)
    customer_name = models.CharField(max_length=50) 
    customer_contact = models.CharField(max_length=20)
    customer_address = models.CharField(max_length=100)
    customer_email = models.CharField(max_length=100)
    items = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    Payment_Method = models.CharField(max_length=15)
    Card_Nummber = models.IntegerField()
    Card_Expiration = models.CharField(max_length=15)
    Card_Cvv = models.IntegerField()
    def __str__(self):
        return f'{self.id} {self.customer_name} {self.user} '
    

    @property
    def prod_qty(self):
        prods = self.items
        prod_list = ast.literal_eval(prods)
        newlist = [] # empty list to hold unique elements from the list
        duplist = [] # empty list to hold the duplicate elements from the list
        for i in prod_list:
            if i not in newlist:
                newlist.append(i)
            else:
                duplist.append(i)
                 
        return duplist
    