from django.urls import path
from .views import CertificationListView, CertificationDetailView

urlpatterns = [
    path('', CertificationListView.as_view(), name='certification-list'),
    path('<int:pk>/', CertificationDetailView.as_view(), name='certification-detail'),
]
