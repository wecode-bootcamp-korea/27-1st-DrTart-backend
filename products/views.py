from django.http      import JsonResponse
from django.views     import View
from django.db.models import Sum, Q

from products.models  import Product

class ProductView(View):
    def get(self, request):
        try:
            menu     = request.GET.get('menu', None)
            category = request.GET.get('category', None)
            limit    = int(request.GET.get('limit', 100))
            offset   = int(request.GET.get('offset', 0))
            
            q = Q()
            category_mapping = None
            mapping = {
                "menu"     : "category__menu",
                "category" : "category"
            }
            
            if menu:
                q &= Q(category__menu__name=menu)
                category_mapping = mapping["menu"]
                        
            if category:
                q &= Q(category__name=category) 
                category_mapping = mapping["category"]

            products = Product.objects.select_related(category_mapping)\
                    .annotate(sum=Sum('orderitem__quantity'))\
                    .filter(q).order_by('-sum')[offset:limit+offset]
                    
            product_list = [
                    {'id'                 : product.id,
                    'korean_name'         : product.korean_name,
                    'price'               : product.price,
                    'thumbnail_image_url' : product.thumbnail_image_url,
                    'vegan_or_not'        : product.vegan_or_not,
                    'category'            :{
                            'name'     : product.category.menu.name,
                            'category' : product.category.name
                        },
                    'created_at'          : product.created_at,
                    'like'                : 'TEMPORARY_LIKES',
                    'order_quantity'      : product.order.quantity,
                    
                } for product in products]
                    
            return JsonResponse({'product_list': product_list}, status = 200)
            
        except Product.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=404)
        
        except AttributeError:
            return JsonResponse({'message' : 'AttributeError'}, status=400)
        
        except TypeError:
            return JsonResponse({'message' : 'TypeError'}, status=400)
        
    