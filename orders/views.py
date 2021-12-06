import json

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from .models                import Cart,OrderStatus,Order,OrderItem


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
        except:
            a=1