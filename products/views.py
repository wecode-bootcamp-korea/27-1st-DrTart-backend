from django.http import JsonResponse
from django.views import View
from django.db.models import Sum

from products.models import Product

class ProductView(View):
    def get(self, request):
        try:
            product_list = []
            main = request.GET.get('main', None)
            all = request.GET.get('all', None)
            menu = request.GET.get('menu', None)
            category = request.GET.get('category', None)
            products=[]
            if main:
                products = Product.objects.all().annotate(sum=Sum('orderitem__quantity')).order_by('-sum')[:5]
            if all:
                products = Product.objects.all().annotate(sum=Sum('orderitem__quantity')).order_by('-sum')
            if menu:
                products = Product.objects.filter(category__menu__name=menu).annotate(sum=Sum('orderitem__quantity')).order_by('-sum')
            if category:
                products = Product.objects.filter(category__name=category).annotate(sum=Sum('orderitem__quantity')).order_by('-sum')
            
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
                    
            return JsonResponse({'product_list': product_list}, status = 200)
            
        except Product.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=401)
        
        except AttributeError:
            return JsonResponse({'message' : 'AttributeError'}, status=400)
        
        except TypeError:
            return JsonResponse({'message' : 'TypeError'}, status=400)
        