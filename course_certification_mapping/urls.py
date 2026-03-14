from django.urls import path
from .views import CourseCertificationMappingListView, CourseCertificationMappingDetailView

urlpatterns = [
    path('', CourseCertificationMappingListView.as_view(), name='course-certification-mapping-list'),
    path('<int:pk>/', CourseCertificationMappingDetailView.as_view(), name='course-certification-mapping-detail'),
]
