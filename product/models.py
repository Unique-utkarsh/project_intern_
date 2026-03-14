from django.db import models
from core.base_models import MasterModel


class Product(MasterModel):
    class Meta:
        db_table = 'product'
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
