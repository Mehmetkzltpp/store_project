from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import CheckoutSerializer
from rest_framework import filters

# Create your views here.

# STOREFRONT ENGINE

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    #activating search and ordering filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    #defining which database columns the user is allowed to search through
    search_fields = ['name', 'descriptipn', 'category__name']

    #defining which columns the user can use to sort data
    order_fields = ['price', 'stock_quantity']

# SINGLE PRODUCT MANAGER

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        current_user = request.user
        items_to_buy = serializer.validated_data['items']


        with transaction.atomic():

            order = Order.objects.create(user=current_user, total_price=0)
            running_total = 0

            for item in items_to_buy:
                prod_id = item['product_id']
                qty_requested = item['quantity']

                try:
                    product = Product.objects.get(id=prod_id)
                except Product.DoesNotExist:
                    return Response({"error": f"Product ID {prod_id} not found."}, status=status.HTTP_404_NOT_FOUND)

                if product.stock_quantity < qty_requested:
                    return Response(
                        {
                            "error": f"Inadequate stock for '{product.name}'. Available: {product.stock_quantity}, Requested: {qty_requested}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # deducting inventory
                product.stock_quantity -= qty_requested
                product.save()

                # Calculates subtotal cost
                item_price = product.price
                running_total += item_price * qty_requested

                #
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty_requested,
                    price_at_purchase=item_price
                )


            order.total_price = running_total
            order.save()

        return Response({
            "message": "Order placed successfully!",
            "order_id": order.id,
            "total_price": str(order.total_price)
        }, status=status.HTTP_201_CREATED)

    #