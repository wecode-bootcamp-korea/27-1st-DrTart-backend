from django.db import models
from django.db.models.expressions import OrderBy
from django.db.models.deletion    import CASCADE

from users.models    import User
from products.models import Product

class Cart(models.Model):
    product      = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    quantity     = models.IntegerField(default=0)
    price        = models.IntegerField()
    
    class Meta:
        db_table = 'carts'
        
class Orderstatus(models.Model):
    status = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'orderstatus'
        
class Order(models.Model):
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)
    address      = models.CharField(max_length=100)
    order_status = models.ForeignKey('Orderstatus', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'orders'
        
class Orderitem(models.Model):
    order    = models.ForeignKey('Order', on_delete=models.CASCADE)
    product  = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'orderitems'