from django.db import models
from core.base_models import TimeStampedModel
from vendor.models import Vendor
from product.models import Product


class VendorProductMapping(TimeStampedModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_vendors')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'vendor_product_mapping'
        unique_together = [('vendor', 'product')]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vendor.name} -> {self.product.name}"
