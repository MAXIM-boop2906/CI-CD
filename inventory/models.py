from django.db import models

class Product(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Stock(models.Model):
    address = models.CharField("Адрес склада", max_length=512)

    products = models.ManyToManyField(
        Product,
        through="StockProduct",
        related_name="stocks",
        verbose_name="Товары",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return self.address


class StockProduct(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="stock_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_stocks")
    price = models.DecimalField("Стоимость хранения", max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["stock", "product"], name="unique_product_per_stock")
        ]
        verbose_name = "Товар на складе"
        verbose_name_plural = "Товары на складах"

    def __str__(self):
        return f"{self.product} — {self.stock} ({self.price})"
