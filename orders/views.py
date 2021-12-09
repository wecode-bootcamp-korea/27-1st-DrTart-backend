import json

from enum               import Enum

from django.db.utils    import IntegrityError
from django.http        import JsonResponse
from django.http.cookie import parse_cookie
from django.views       import View
from django.db          import DatabaseError, transaction
from django.db.models   import Sum, F

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
    def patch(self, request):
        try:
            data     = json.loads(request.body)
            user     = request.body
            cart_id  = data['cart_id']
            quantity = data['quantity']

            if not Cart.objects.filter(id=cart_id, user=user).exists():
                return JsonResponse({"message" : "CART_NOT_EXIST"}, status=400)
            
            cart = Cart.objects.get(id=cart_id, user=user)

            cart.quantity = quantity
            cart.save()

            if cart.quantity <= 0:
                return JsonResponse({"message" : "QUANTITY_ERROR"}, status=400)

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)


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
    
class OrderStatusEnum(Enum):
    PAID            = 1
    PENDING         = 2
    PREPARING       = 3
    SHIPPEND        = 4
    DELIVERD        = 5
    ORDER_CANCELLED = 6
    
class OrderView(View):
    @authorization
    def post(self, request):
        data     = json.loads(request.body)
        user     = request.user
        items    = data

        try: 
            with transaction.atomic():
                order = Order.objects.create(  
                    address      = User.objects.get(id=user.id).address,
                    user         = user,
                    order_status = OrderStatus.objects.get(id=OrderStatusEnum.PENDING.value)
                )   
                
                order_items = [OrderItem(
                    order      = order,
                    product_id = item['product_id'],
                    quantity   = item['quantity']
                ) for item in items]
                
                OrderItem.objects.bulk_create(order_items)
            
                carts = Cart.objects.filter(user = user)                
                carts.delete() 

            return JsonResponse({'message':order.id}, status=201)
        
        except transaction.TransactionManagementError:
            return JsonResponse({'message':'TransactionManagementError'}, status=401)                                                                                                                      
        
    @authorization
    def get(self, request):
        user        = request.user
        order       = request.GET.get('id',)
        order_items = Order.objects.get(id=order).orderitem_set.all()
        total_price = int(Order.objects.filter(id=order).annotate(total=Sum(F('orderitem__product__price')*F('orderitem__quantity')))[0].total)
    
        order_list = [{
            'order_id'     : order,
            'user'         : User.objects.get(id=user.id).name,
            'address'      : Order.objects.get(id=order).address,
            'order_items'  : [{
                'product_id'    : order_item.product.id,
                'quantity'      : order_item.quantity,
                'product_name'  : order_item.product.korean_name,
                'product_image' : order_item.product.thumbnail_image_url,
                'price'         : int((order_item.quantity) * (order_item.product.price))
            } for order_item in order_items],
            'total_price'  : total_price
        }]
        
        return JsonResponse({'order_list':order_list}, status=200)

    @authorization
    def patch(self, request):
        data     = json.loads(request.body)
        order_id = data['order_id']  
        
        try:
            Order.objects.filter(id=order_id).update(order_status=OrderStatusEnum.ORDER_CANCELLED.value)
            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
    
    