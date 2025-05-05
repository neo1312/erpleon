from django.db import models
from core.models.base import TimeStampedModel

class Brand(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
