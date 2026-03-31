SECRET_KEY='django-insecure--2)f%27lxkok^zguxk)v*=qtmu1)%yz3n3si!o*0$8!z6l%g3('
DATABASES = {
        'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dr_tart',
        'USER': 'root',
        'PASSWORD': '19930905',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}
     }
}
ALGORITHM = 'HS256'
