from django.db import models
from core.base_models import MasterModel


class Course(MasterModel):
    class Meta:
        db_table = 'course'
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
