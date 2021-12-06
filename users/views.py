import json, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from .models                import User
from core.validators        import email_validate, password_validate


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email_validate(data['email'])
            password_validate(data['password'])

            if User.objects.filter(email = data['email']).exists():
                return ValidationError('DUPLICATED_EMAIL')

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = hashed_password,
                address      = data['address'],
                vegan_or_not = data['vegan_or_not']
            )
            return JsonResponse({'message':'SUCCESS'},status=201)

        except ValidationError as e:
            return JsonResponse({'message': e.message},status=400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)


