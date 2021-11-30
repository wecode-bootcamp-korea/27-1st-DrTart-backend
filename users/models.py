from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=100)
    email        = models.CharField(max_length=250, unique=True)
    password     = models.CharField(max_length=300)
    address      = models.CharField(max_length=100)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    vegan_or_not = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users'
