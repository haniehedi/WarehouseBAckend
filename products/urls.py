# products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('wares', views.WareModelViewSet, basename='wares')
router.register('warehouses', views.WarehouseModelViewSet, basename='warehouses')
router.register('factors', views.FactorModelViewSet, basename='factors')

urlpatterns = [
    path('', include(router.urls)),
]
