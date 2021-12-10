from django.urls import path

from products.views import ProductView, ProductDetailView, LikeView


urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/<int:product_id>/like', LikeView.as_view()),
]
