from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, Stock, StockProduct

class InventoryAPITests(APITestCase):
    def test_product_crud_and_search(self):
        response = self.client.post("/products/", {
            "name": "Помидоры", "description": "Красные овощи"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_id = response.data["id"]
        search = self.client.get("/products/?search=помид")
        self.assertEqual(search.status_code, status.HTTP_200_OK)
        self.assertEqual(search.data["count"], 1)
        detail = self.client.get(f"/products/{product_id}/")
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        delete = self.client.delete(f"/products/{product_id}/")
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_stock_nested_products_and_search(self):
        product = Product.objects.create(name="Помидоры", description="Свежие")
        response = self.client.post("/stocks/", {
            "address": "Тестовый склад",
            "products": [{"id": product.id, "price": "12.50"}]
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        stock_id = response.data["id"]
        self.assertEqual(StockProduct.objects.filter(stock_id=stock_id).count(), 1)
        by_id = self.client.get(f"/stocks/?products={product.id}")
        self.assertEqual(by_id.data["count"], 1)
        by_name = self.client.get("/stocks/?search=помид")
        self.assertEqual(by_name.data["count"], 1)
