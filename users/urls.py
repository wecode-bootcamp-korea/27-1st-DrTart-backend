from django.urls import path

from .views import SigninView, SignupView

urlpatterns = [
    path('/signup', SignupView.as_view()),
]
