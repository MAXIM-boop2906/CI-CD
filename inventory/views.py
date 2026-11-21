from django.db.models import Q
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "description"]


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    filter_backends = []

    def get_queryset(self):
        queryset = Stock.objects.prefetch_related("stock_products__product").all()
        product_id = self.request.query_params.get("products")
        if product_id:
            queryset = queryset.filter(stock_products__product_id=product_id)
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(stock_products__product__name__icontains=search)
                | Q(stock_products__product__description__icontains=search)
            )
        return queryset.distinct()
