from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.views import ProductViewSet, StockViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")
router.register("stocks", StockViewSet, basename="stock")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api/", include(router.urls)),
]
