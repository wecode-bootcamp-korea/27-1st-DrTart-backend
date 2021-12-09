import json
from django.db.utils import IntegrityError

from django.http        import JsonResponse
from django.http.cookie import parse_cookie
from django.views       import View
from django.db          import DatabaseError, transaction

from users.models    import User
from products.models import Product
from orders.models   import Cart, Order, OrderItem, OrderStatus
from core.utils      import authorization

class CartView(View):
    @authorization
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            product_id = data['product_id']
            quantity   = data['quantity']
            print(44)
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({"message" : "PRODUCT_NOT_EXIST"}, status=400)
            
            cart, created  = Cart.objects.get_or_create(
                user       = user,
                product_id = product_id
            )
            cart.quantity  += quantity
            cart.save()
            
            if cart.quantity <= 0 :
                return JsonResponse({"message" : "QUANTITY_ERROR"}, status=400)
            
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({"message" : "INVALID_CART"}, status=400)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
         
    @authorization
    def get(self, request):

        user  = request.user
        carts = Cart.objects.select_related('product').filter(user=user)
        if not Cart.objects.filter(user=user).exists():
            return JsonResponse({"message" : "CART_NOT_EXIST"}, status=400)
        
        result = [{
            'cart_id'             : cart.id,
            'product_id'          : cart.product.id,
            'korean_name'         : cart.product.korean_name,
            'price'               : int(cart.product.price),
            'thumbnail_image_url' : cart.product.thumbnail_image_url,
            'quantity'            : cart.quantity
        } for cart in carts ]

        return JsonResponse({"cart_info" : result}, status=200)

    @authorization
    def delete(self, request):
        
        data    = json.loads(request.body)  
        user    = request.user
        cart_id = data['cart']
        cart    = Cart.objects.get(id = cart_id, user = user)

        if not Cart.objects.filter(id = cart_id, user = user).exists():
            return JsonResponse({"message" : "NOT_EXIST"}, status=400)
        
        cart.delete()

        return JsonResponse({"message" : "DELETE_SUCCESS"}, status=204)
    
class OrderView(View):
    @authorization
    def post(self, request):

        data     = json.loads(request.body)
        user     = request.user
        items    = data

        try: 
            with transaction.atomic():
                PENDING = OrderStatus.objects.get(id=2)
                    
                order = Order.objects.create(  
                    address      = User.objects.get(id=user.id).address,
                    user         = user,
                    order_status = PENDING
                )   
                
                order_items = [OrderItem(
                    order      = order,
                    product_id = item['product_id'],
                    quantity   = item['quantity']
                ) for item in items]
                
                OrderItem.objects.bulk_create(order_items)
            
                carts = Cart.objects.filter(user = user)                
                carts.delete() 

            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except IntegrityError:
            return JsonResponse({'message':'INTEGRITY_ERROR'}, status=401)                                                                                                                      
        
    @authorization
    def get(self, request):
        user = request.user
        order = Order.objects.filter(user=user).order_by('-created_at')[0]
        order_items = order.orderitem_set.all()
        
        total_price_list = []
        for order_item in order_items:
            a = order_item.quantity * order_item.product.price
            total_price_list.append(a)
        

        order_list = [{
            'order_id'     : order.id,
            'user'         : User.objects.get(id=user.id).name,
            'address'      : order.address,
            'order_items'  : [{
                'product_id'    : order_item.product.id,
                'quantity'      : order_item.quantity,
                'product_name'  : order_item.product.korean_name,
                'product_image' : order_item.product.thumbnail_image_url,
                'price'         : int((order_item.quantity) * (order_item.product.price))
            } for order_item in order_items],
            'total_price'  : int(sum(total_price_list))
        }]
        
        return JsonResponse({'order_list':order_list}, status=200)

    @authorization
    def patch(self, request):
        data = json.loads(request.body)
        order_id = data['order_id']  
        
        CANCELED = OrderStatus.objects.filter(id=6)
        
        if order_id:
            Order.objects.filter(id=order_id).update(order_status=CANCELED)
            
        return JsonResponse({'message':'SUCCESS'}, status=200)
