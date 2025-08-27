from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    hospital = models.CharField(max_length=200)
    diagnoses = models.TextField()
    disease = models.CharField(max_length=200)
    lab_tests = models.TextField(null=True, blank=True)
    medicine = models.TextField()

    def __str__(self):
        return f"{self.disease} - {self.hospital}"
    
