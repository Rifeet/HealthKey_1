from django.db import models

# Create your models here.
# authentication/models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta

class OTPCode(models.Model):
    national_id = models.CharField(max_length=32, db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.national_id} - {self.code}"
