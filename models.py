from django.db import models
# user : Ashar Pass:123

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=25,default="")
    category_image = models.ImageField(upload_to='ecom/images',default="")
    
    
    def __str__(self):
        return self.category_name


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
    Name_Cart = models.CharField(max_length=25)
    Category_Cart = models.ForeignKey(Category, on_delete=models.CASCADE)        
    Price_Cart = models.IntegerField()
    Image_Cart = models.ImageField(upload_to='ecom/images')
    def __str__(self):
        return self.Name_Cart