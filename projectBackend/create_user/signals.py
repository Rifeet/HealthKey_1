# create_user/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

# Import the models you need
from .models import Emergency

# Signal function to auto-fill fields before saving an Emergency
@receiver(pre_save, sender=Emergency)
def fill_emergency_fields(sender, instance, **kwargs):
    if instance.patient:
        instance.blood_group = instance.patient.blood_group
        instance.chronic_conditions = ", ".join([d.name for d in instance.patient.chronic_conditions.all()])
        instance.allergies = instance.patient.allergies
        # Prescriptions example: get current active prescriptions
        instance.prescriptions_section = ", ".join([
            p.drug.drug_name for p in instance.patient.prescriptions.filter(end_date__gte=timezone.now().date())
        ])
