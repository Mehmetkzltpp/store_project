from django.urls import path
from .views import ProductListCreateView, ProductDetailView, CheckoutAPIView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('checkout/', CheckoutAPIView.as_view(), name='checkout')
]