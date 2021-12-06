from django.http import JsonResponse
from django.views import View
from django.db.models import Sum

from products.models import Product,Menu

class ProductMainView(View):
    def get(self, request):
        products = Product.objects.all().annotate(sum=Sum('orderitem__quantity')).order_by('-sum')
        product_list = []
        for product in products:
            product_list.append({
                'id': product.id,
                'korean_name'         : product.korean_name,
                'price'               : product.price,
                'thumbnail_image_url' : product.thumbnail_image_url,
                'vegan_or_not'        : product.vegan_or_not,
                'category'            :{
                        'name'     : product.category.menu.name,
                        'category' : product.category.name
                    },
                'created_at'          : product.created_at
            })
        
        return JsonResponse({'product_list' : product_list}, status=200)
    
class ProductAllView(View):
    def get(self,request):
        products = Product.objects.all()
        
        try:
            product_list = []               
            for product in products:
                a = product.orderitem_set.all().values('product').annotate(product_quantity=Sum('quantity'))
                for i in a:
                    product_list.append({
                        'id'           : product.id,
                        'korean_name'  : product.korean_name,
                        'price'        : product.price,
                        'thumbnail_image_url' : product.thumbnail_image_url,
                        'vegan_or_not' : product.vegan_or_not,
                        'category'     :{
                                'name'     : product.category.menu.name,
                                'category' : product.category.name
                            },
                        'order_quantity': i['product_quantity'],
                        'created_at'    : product.created_at
                            
                    })
                    
            return JsonResponse({'product_list': product_list}, status = 201)
        
        except Product.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=401)
        
        
class ProductMenuView(View):
    def get(self,request):
        menu = request.GET.get('menu_name', None)
        products = Product.objects.filter(category__menu__name=menu)
        
        try:
            product_list = []
            if menu:
                for product in products:
                    a = product.orderitem_set.all().values('product').annotate(product_quantity=Sum('quantity'))
                    for i in a:
                        product_list.append({
                            'id'                  : product.id,
                            'korean_name'         : product.korean_name,
                            'price'               : product.price,
                            'thumbnail_image_url' : product.thumbnail_image_url,
                            'vegan_or_not'        : product.vegan_or_not,
                            'category'            : product.category.id,
                            'menu'                : product.category.menu.name, 
                            'order_quantity'      : i['product_quantity'],
                            'created_at'          : product.created_at
                                
                        })
                    
            return JsonResponse({'product_list': product_list}, status = 201)
        
        except Product.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=401)

class ProductListView(View):
    def get(self,request):
        category = request.GET.get('category_name', None)
        products = Product.objects.filter(category__name=category)

        try:
            product_list = []
            if category:   
                for product in products:
                    a = product.orderitem_set.all().values('product').annotate(product_quantity=Sum('quantity'))
                    for i in a:
                        product_list.append({
                            'id'                  : product.id,
                            'korean_name'         : product.korean_name,
                            'price'               : product.price,
                            'thumbnail_image_url' : product.thumbnail_image_url,
                            'vegan_or_not'        : product.vegan_or_not,
                            'category'            : product.category.id, 
                            'order_quantity'      : i['product_quantity'],
                            'created_at'          : product.created_at
                                
                        })
                    
            return JsonResponse({'product_list': product_list}, status = 201)
        
        except Product.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=401)
        
    
class ProductDetailView(View):
    def get(self,request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            images = product.image_set.filter(product__id=product_id)
            data = {
                    'korean_name'         : product.korean_name,
                    'price'               : product.price,
                    'thumbnail_image_url' : product.thumbnail_image_url,
                    'vegan_or_not'        : product.vegan_or_not,
                    'sugar_level'         : product.sugar_level,
                    'category'            : product.category.name,
                    'description'         : product.description, 
                    'image_list'          : [{
                        'id' : image.id,
                        'url': image.url
                    } for image in images]
                }
                
            return JsonResponse({'product_list':data}, status = 201)
                
        except Product.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=401)