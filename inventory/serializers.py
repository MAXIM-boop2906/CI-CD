from rest_framework import serializers
from .models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description"]


class StockProductInputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)


class StockProductOutputSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="product.id", read_only=True)
    name = serializers.CharField(source="product.name", read_only=True)
    description = serializers.CharField(source="product.description", read_only=True)

    class Meta:
        model = StockProduct
        fields = ["id", "name", "description", "price"]


class StockSerializer(serializers.ModelSerializer):
    products = StockProductInputSerializer(many=True, write_only=True, required=False)
    product_list = StockProductOutputSerializer(source="stock_products", many=True, read_only=True)

    class Meta:
        model = Stock
        fields = ["id", "address", "products", "product_list"]

    def _save_products(self, stock, products_data):
        seen_ids = set()
        for item in products_data:
            product_id = item["id"]
            if product_id in seen_ids:
                raise serializers.ValidationError(
                    {"products": f"Продукт с id={product_id} указан несколько раз."}
                )
            seen_ids.add(product_id)
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    {"products": f"Продукт с id={product_id} не существует."}
                )
            StockProduct.objects.update_or_create(
                stock=stock,
                product=product,
                defaults={"price": item["price"]},
            )
        stock.stock_products.exclude(product_id__in=seen_ids).delete()

    def create(self, validated_data):
        products_data = validated_data.pop("products", [])
        stock = Stock.objects.create(**validated_data)
        self._save_products(stock, products_data)
        return stock

    def update(self, instance, validated_data):
        products_data = validated_data.pop("products", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if products_data is not None:
            self._save_products(instance, products_data)
        return instance
