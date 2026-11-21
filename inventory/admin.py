from django.contrib import admin
from .models import Product, Stock, StockProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", "description")

class StockProductInline(admin.TabularInline):
    model = StockProduct
    extra = 1

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "address")
    inlines = [StockProductInline]
