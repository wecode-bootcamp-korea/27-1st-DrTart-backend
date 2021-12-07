import json

from django.http        import JsonResponse
from django.http.cookie import parse_cookie
from django.views       import View

from products.models import Product
from orders.models   import Cart
from core.utils      import authorization

class CartView(View):
    @authorization
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            product_id = data['product_id']
            quantity   = data['quantity']
            
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({"message" : "PRODUCT_NOT_EXIST"}, status=400)
            
            if quantity <= 0 :
                return JsonResponse({"message" : "QUANTITY_ERROR"}, status=400)
            
            cart, created  = Cart.objects.get_or_create(
                user       = user,
                product_id = product_id
            )
            cart.quantity += quantity
            cart.save()
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({"message" : "INVALID_CART"}, status=400)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
         
    @authorization
    def get(self, request):

        user  = request.user
        carts = Cart.objects.select_related('product__korean_name','product__price','product__thumbnail_image_url').filter(user=user)
        if not Cart.objects.filter(user=user).exists():
            return JsonResponse({"message" : "CART_NOT_EXIST"}, status=400)
        
        result = [{
            'cart_id'             : cart.id,
            'korean_name'         : cart.product.korean_name,
            'price'               : cart.product.price,
            'thumbnail_image_url' : cart.product.thumbnail_image_url,
            'quantity'            : cart.quantity
        } for cart in carts]

        return JsonResponse({"cart_info" : result}, status=200)

    @authorization
    def patch(self, request):
        try:
            data     = json.loads(request.body)
            user     = request.user
            cart_id  = data['cart_id']
            quantity = data['quantity']
            
            if not Cart.objects.filter(id=cart_id, user=user).exists():
                return JsonResponse({"message" : "CART_NOT_EXIST"}, status=400)

            if quantity <= 0:
                return JsonResponse({"message" : "QUANTITY_ERROR"}, status=400)

            cart = Cart.objects.get(id = cart_id, user = user)
            cart.product_id = data['product_id']

            cart.quantity = quantity
            cart.save()
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    
    @authorization
    def delete(self, request, cart_id):
          
        user = request.user
        cart = Cart.objects.get(id = cart_id, user = user)

        if not Cart.objects.filter(id = cart_id, user = user).exists():
            return JsonResponse({"message" : "NOT_EXIST"}, status=400)
        
        cart.delete()

        return JsonResponse({"message" : "DELETE_SUCCESS"}, status=201)

