from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
            ],
            options={"ordering": ["id"], "verbose_name": "Товар", "verbose_name_plural": "Товары"},
        ),
        migrations.CreateModel(
            name="Stock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("address", models.CharField(max_length=512, verbose_name="Адрес склада")),
            ],
            options={"ordering": ["id"], "verbose_name": "Склад", "verbose_name_plural": "Склады"},
        ),
        migrations.CreateModel(
            name="StockProduct",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Стоимость хранения")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="product_stocks", to="inventory.product")),
                ("stock", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="stock_products", to="inventory.stock")),
            ],
            options={"verbose_name": "Товар на складе", "verbose_name_plural": "Товары на складах"},
        ),
        migrations.AddConstraint(
            model_name="stockproduct",
            constraint=models.UniqueConstraint(fields=("stock", "product"), name="unique_product_per_stock"),
        ),
        migrations.AddField(
            model_name="stock",
            name="products",
            field=models.ManyToManyField(related_name="stocks", through="inventory.StockProduct", to="inventory.product", verbose_name="Товары"),
        ),
    ]
