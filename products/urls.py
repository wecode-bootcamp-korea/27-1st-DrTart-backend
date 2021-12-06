from django.urls import path

from products.views import ProductMainView, ProductListView,ProductAllView, ProductMenuView, ProductDetailView


urlpatterns = [
    path('/main', ProductMainView.as_view()),
    path('/all', ProductAllView.as_view()),
    path('/menu', ProductMenuView.as_view()),
    path('/menu/list', ProductListView.as_view()),
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
]
