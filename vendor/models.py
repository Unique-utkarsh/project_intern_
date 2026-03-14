from django.db import models
from core.base_models import MasterModel


class Vendor(MasterModel):
    class Meta:
        db_table = 'vendor'
        ordering = ['-created_at']
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
