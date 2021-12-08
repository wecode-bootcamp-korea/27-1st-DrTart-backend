from django.urls import path

from .views import SigninView, SignupView , IdCheckingView

urlpatterns = [   
    path('/signin', SigninView.as_view()),
    path('/signup', SignupView.as_view()),
    path('/idcheck', IdCheckingView.as_view()),
]