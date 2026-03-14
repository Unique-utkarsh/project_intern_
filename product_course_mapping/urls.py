from django.urls import path
from .views import ProductCourseMappingListView, ProductCourseMappingDetailView

urlpatterns = [
    path('', ProductCourseMappingListView.as_view(), name='product-course-mapping-list'),
    path('<int:pk>/', ProductCourseMappingDetailView.as_view(), name='product-course-mapping-detail'),
]
