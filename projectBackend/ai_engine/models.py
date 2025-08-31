from django.db import models
from create_user.models import Patient
# ai_engine/models.py


class PatientFeatures(models.Model):
    patient = models.OneToOneField(
        "create_user.Patient",   # reference to Patient in create_user app
        on_delete=models.CASCADE,
        related_name="features"
    )

    # Demographics
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, blank=True, null=True)
    BMI = models.FloatField(default=0.0)

    # Lifestyle
    smoking = models.CharField(
        max_length=3, choices=[("yes", "Yes"), ("no", "No")], default="no"
    )
    physical_activity = models.CharField(
        max_length=10,
        choices=[
            ("low", "Low"),
            ("moderate", "Moderate"),
            ("high", "High"),
        ],
        default="moderate"
    )

    # Lab results
    glucose = models.FloatField(default=90.0)  # normal fasting value
    HbA1c = models.FloatField(default=5.0)     # normal %
    cholesterol = models.FloatField(default=180.0)
    blood_pressure_systolic = models.FloatField(default=120.0)
    blood_pressure_diastolic = models.FloatField(default=80.0)
    creatinine = models.FloatField(default=1.0)
    microalbuminuria = models.CharField(max_length=20, blank=True, null=True)
    c_peptide = models.FloatField(default=2.0)

    # Family & history
    diabetes_in_family = models.CharField(
        max_length=3, choices=[("yes", "Yes"), ("no", "No")], default="no"
    )
    previous_diagnoses = models.TextField(blank=True, null=True)   # comma-separated names
    drug_history = models.TextField(blank=True, null=True)         # comma-separated names

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Features for {self.patient.full_name}"
    

class PredictionResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="predictions")
    prediction = models.IntegerField(choices=[(0, "Healthy"), (1, "Diabetic")], default=0,help_text="0=Healthy, 1=Diabetic")
    probability = models.FloatField()
    risk_level = models.CharField(max_length=50)
    recommendation = models.TextField()
    prediction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.patient.full_name}: {self.risk_level} ({self.probability})"    