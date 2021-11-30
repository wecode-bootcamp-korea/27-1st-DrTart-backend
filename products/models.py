from django.db import models

from users.models  import User

class Category(models.Model):
    name   = models.CharField(max_length=50)

class Product(models.Model):
    korean_name  = models.CharField(max_length=20)
    english_name = models.CharField(max_length=20)
    image        = models.URLField(max_length=200)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)
    vegan_or_not = models.BooleanField
    sugar_level  = models.IntegerField
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    description  = models.CharField(max_length=1000)
    
class Image(models.Model):
    url       = models.URLField(max_length=200)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    
class Review(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    content     = models.CharField(max_length=200, null=True)
    
class ReviewComment(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    review      = models.ForeignKey(Review, on_delete=models.CASCADE)
    content     = models.CharField(max_length=100, null=True)
    
class Like(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
