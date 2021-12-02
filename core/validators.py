import re

from django.core.exceptions import ValidationError

def is_blank(email, password):
    if email is None:
        raise KeyError('EMAIL_IS_NULL')
    if password is None:
        raise KeyError('PASSWORD_IS_NULL')

def email_validate(email):
    regexr_email = '[a-zA-Z0-9]+\.?\w*@\w+[.]?\w*[.]+\w{2,3}'
    if not re.match(regexr_email, email):
        raise ValidationError('INVALID_KEY')

def password_validate(password):
    regexr_password = '(?=.*[A-Za-z])(?=.*\d)(?=.*[~!@#$^&*()+|=])[A-Za-z\d~!@#$%^&*()+|=]{8,}'
    if not re.match(regexr_password,password):
        raise ValidationError('INVALID_KEY')