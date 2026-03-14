from django.urls import path
from .views import VendorProductMappingListView, VendorProductMappingDetailView

urlpatterns = [
    path('', VendorProductMappingListView.as_view(), name='vendor-product-mapping-list'),
    path('<int:pk>/', VendorProductMappingDetailView.as_view(), name='vendor-product-mapping-detail'),
]
