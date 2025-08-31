# ai_engine/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from .models import PatientFeatures
from create_user.models import Patient, LabTestResult, Lifestyle, Diagnosis, Prescription

# --- Utility Functions ---
def calculate_age(dob):
    if dob:
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return 0

def calculate_bmi(height, weight):
    if height and weight:
        try:
            return round(weight / ((height/100) ** 2), 2)
        except ZeroDivisionError:
            return 0.0
    return 0.0

# --- Patient Demographics ---
@receiver(post_save, sender=Patient)
def create_or_update_patient_features(sender, instance, created, **kwargs):
    features, _ = PatientFeatures.objects.get_or_create(patient=instance)
    features.age = calculate_age(instance.dob)
    features.gender = instance.gender
    features.BMI = calculate_bmi(instance.height, instance.weight)
    features.save()

# --- Lab Test Updates ---
@receiver(post_save, sender=LabTestResult)
def update_features_from_lab(sender, instance, **kwargs):
    print("Signal triggered for:", instance.patient.full_name)
    print("Lab test:", instance.lab_test.test_code, "Value:", instance.result_value)

    features, _ = PatientFeatures.objects.get_or_create(patient=instance.patient)
    test_code = instance.lab_test.test_code.lower()
    value = instance.result_value

    # Handle numeric tests
    numeric_tests = ["glucose", "hba1c", "cholesterol", "bps", "systolic", "bpd", "diastolic", "creatinine", "cpeptide", "c_peptide"]
    
    if test_code in numeric_tests:
        try:
            features_field_map = {
                "glucose": "glucose",
                "hba1c": "HbA1c",
                "cholesterol": "cholesterol",
                "bps": "blood_pressure_systolic",
                "systolic": "blood_pressure_systolic",
                "bpd": "blood_pressure_diastolic",
                "diastolic": "blood_pressure_diastolic",
                "creatinine": "creatinine",
                "cpeptide": "c_peptide",
                "c_peptide": "c_peptide",
            }
            setattr(features, features_field_map[test_code], float(value))
        except ValueError:
            pass  # skip invalid numeric values
    # Handle string-based tests
    elif test_code in ["microalb", "microalbuminuria"]:
        features.microalbuminuria = value  # store "Normal", "High", "Elevated" directly

    features.save()

# --- Lifestyle, Diagnosis, Prescription Updates ---
def update_patient_features(patient):
    features, _ = PatientFeatures.objects.get_or_create(patient=patient)

    # Lifestyle
    lifestyle = patient.lifestyles.order_by("-created_at").first()
    if lifestyle:
        features.diabetes_in_family = lifestyle.diabetes_in_family
        features.smoking = lifestyle.smoking
        features.physical_activity = lifestyle.physical_activity
    else:
        features.diabetes_in_family = "no"
        features.smoking = "no"
        features.physical_activity = "moderate"

    # Previous Diagnoses
    diagnoses = patient.visits.prefetch_related("diagnoses").values_list("diagnoses__disease__name", flat=True)
    features.previous_diagnoses = ", ".join(set(filter(None, diagnoses)))

    # Drug history
    drugs = patient.prescriptions.values_list("drug__drug_name", flat=True)
    features.drug_history = ", ".join(set(drugs))

    features.save()

# Signals
@receiver(post_save, sender=Lifestyle)
def lifestyle_post_save(sender, instance, **kwargs):
    update_patient_features(instance.patient)

@receiver(post_save, sender=Diagnosis)
def diagnosis_post_save(sender, instance, **kwargs):
    update_patient_features(instance.visit.patient)

@receiver(post_save, sender=Prescription)
def prescription_post_save(sender, instance, **kwargs):
    update_patient_features(instance.patient)
