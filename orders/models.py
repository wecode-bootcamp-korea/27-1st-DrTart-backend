from django.db import models

class Cart(models.Model):
    product      = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    quantity     = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'carts'
        
class OrderStatus(models.Model):
    status = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'order_status'
        
class Order(models.Model):
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True, null=True)
    updated_at   = models.DateTimeField(auto_now=True, null=True)
    address      = models.CharField(max_length=100)
    order_status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'orders'
        
class OrderItem(models.Model):
    order        = models.ForeignKey('Order', on_delete=models.CASCADE)
    product      = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity     = models.IntegerField(default=1)
    created_at   = models.DateTimeField(auto_now_add=True, null=True)
    updated_at   = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'order_items'