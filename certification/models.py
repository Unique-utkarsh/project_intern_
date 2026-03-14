from django.db import models
from core.base_models import MasterModel


class Certification(MasterModel):
    class Meta:
        db_table = 'certification'
        ordering = ['-created_at']
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'
