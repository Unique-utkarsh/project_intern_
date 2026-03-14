from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base model with timestamp fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MasterModel(TimeStampedModel):
    """Abstract base model for all master entities."""
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} ({self.code})"
