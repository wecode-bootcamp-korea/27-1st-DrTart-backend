import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Sum, Q
from core.utils import AuthorizeProduct, authorization

from products.models  import Product, Like

class ProductView(View):
    @AuthorizeProduct
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
                        .annotate(sum=Sum('orderitem__quantity')).filter(q).order_by('-sum')[offset:limit+offset]
                    
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
                    'like_num'            : product.like_set.count(),
                    'is_like_True'        : True if product.like_set.filter(user_id=request.user).exists() else False,                                                                                                                                                                       
                    'order_quantity'      : product.orderitem_set.all()[0].quantity if product.orderitem_set.all().exists() else 0,
                    
                } for product in products]
                    
            return JsonResponse({'product_list': product_list}, status = 200)
            
        except Product.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=404)
        
        except AttributeError:
            return JsonResponse({'message' : 'AttributeError'}, status=400)
        
        except TypeError:
            return JsonResponse({'message' : 'TypeError'}, status=400)
        
class ProductDetailView(View):
    @AuthorizeProduct
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            images = product.image_set.all()
            data = {
                    'korean_name'         : product.korean_name,
                    'price'               : product.price,
                    'thumbnail_image_url' : product.thumbnail_image_url,
                    'vegan_or_not'        : product.vegan_or_not,
                    'sugar_level'         : product.sugar_level,
                    'category'            : product.category.name,
                    'description'         : product.description, 
                    'like_num'            : Product.objects.filter(like__product_id=product_id).count(),
                    'is_like_True'        : True if product.like_set.filter(user_id=request.user).exists() else False,
                    'image_list'          : [{
                        'id' : image.id,
                        'url': image.url
                    } for image in images]
                }
                
            return JsonResponse({'product_list':data}, status = 201)
                
        except Product.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=401)

class LikeView(View):
    @authorization
    def post(self, request, product_id):
        try:
            like, is_created = Like.objects.get_or_create(user=request.user, product_id=product_id)

            data_status = 201 if is_created else 200

            if is_created:
                return JsonResponse({"message" : "CREATED"}, status=data_status)

            like.delete()
            return JsonResponse({"message" : "DELETED"}, status=data_status)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)