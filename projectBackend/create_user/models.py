from django.db import models
from django.utils import timezone

# Hospital Table.
class Hospital(models.Model):
    hospital_id = models.AutoField(primary_key=True)   # Auto-increment ID
    hospital_name = models.CharField(max_length=255)   # Hospital name
    hospital_branch = models.CharField(max_length=255) # Branch name
    HOSPITAL_TYPE = [
        ('Government', 'Government'),
        ('Private', 'Private'),
    ]
    hospital_type = models.CharField(
        max_length=20,
        choices=HOSPITAL_TYPE,
        default='Government')   # default value if nothing is chosen
    def __str__(self):
        return f"{self.hospital_name} - {self.hospital_branch}"

# Doctor Table.
class Doctor(models.Model):
    national_id = models.CharField(max_length=20, unique=True)  # Added national ID
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # store plain first
    email = models.EmailField(unique=True)
    specialist = models.CharField(max_length=100)
    # ForeignKey to Hospital
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="doctors"
    )

    def __str__(self):
        return f"{self.username} - {self.specialist}"

# Parient Table.
class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    national_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=150)
    dob = models.DateField()  # Date of Birth
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    # Chronic conditions (link to Disease codes)
    chronic_conditions = models.ManyToManyField("Disease", blank=True, related_name="patients")
    # BMI will always be calculated automatically
    '''bmi = models.FloatField(max_length=20, null=True, blank=True)  # Not editable in forms
    
    def save(self, *args, **kwargs):
        if self.height and self.weight:
            # Convert height from cm to meters before calculating BMI
            height_m = self.height / 100
            self.bmi = round(self.weight / (height_m ** 2), 2)
        super().save(*args, **kwargs)
'''
    mobile_number = models.CharField(max_length=15)
    allergies = models.TextField(blank=True, null=True)  # optional field
    
    def __str__(self):
        return f"{self.full_name} ({self.national_id})"

class Disease(models.Model):
    disease_code = models.CharField(max_length=20, unique=True)  # e.g., ICD-10 code
    name = models.CharField(max_length=100)                      # e.g., "Diabetes Mellitus"
    description = models.TextField(blank=True, null=True)        # extra details if needed
    def __str__(self):
        return f"{self.disease_code} - {self.name}"

# Diagnosis Table
class Diagnosis(models.Model):
    SEVERITY_CHOICES = [
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
    ]
    
    visit = models.ForeignKey(
        "Visit",
        on_delete=models.CASCADE,
        related_name="diagnoses"
    )
    
    disease = models.ForeignKey(
        "Disease",
        on_delete=models.CASCADE,
        related_name="diagnoses"
    )
    
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='Mild'
    )
    
    notes = models.TextField(blank=True, null=True)
    diagnosis_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Visit {self.visit.visit_id} - {self.disease.name} ({self.severity})"


    
# visit table  
class Visit(models.Model):
    visit_id = models.AutoField(primary_key=True)  # Auto-increment ID
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # Link to Patient
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)    # Link to Doctor
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE) # Link to Hospital
    notes = models.TextField(blank=True, null=True)  # optional extra notes by doctor
    appointment = models.OneToOneField("Appointment", on_delete=models.SET_NULL, null=True, blank=True)

    visit_date = models.DateTimeField(auto_now_add=True)  # Date and time of visit 
    def __str__(self):
        return f"Visit {self.visit_id} - {self.patient.full_name} with {self.doctor.username}"
    
# Lab Test Table    
class LabTest(models.Model):
    test_code = models.CharField(max_length=20, unique=True)  # e.g., "CBC"
    test_name = models.CharField(max_length=100)              # e.g., "Complete Blood Count"
    description = models.TextField(blank=True, null=True)
    normal_range = models.CharField(max_length=100, blank=True, null=True)  # e.g., "4.5-5.5 million cells/uL"

    def __str__(self):
        return f"{self.test_name} ({self.test_code})"

# Lab Test Result Table
class LabTestResult(models.Model):
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        related_name="lab_results"
    )
    visit = models.ForeignKey(
        "Visit",
        on_delete=models.CASCADE,
        related_name="lab_results",
        null=True, blank=True
    )
    lab_test = models.ForeignKey(
        "LabTest",
        on_delete=models.CASCADE,
        related_name="results"
    )
    result_value = models.CharField(max_length=100)  # e.g., "5.1 million cells/uL"
    result_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.lab_test.test_name} for {self.patient.full_name}: {self.result_value}"


# Appointment Table
class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)   # Who booked
    doctor = models.ForeignKey("Doctor", on_delete=models.SET_NULL, null=True)  # With which doctor
    hospital = models.ForeignKey("Hospital", on_delete=models.CASCADE) # At which branch
    appointment_date = models.DateTimeField()      # Scheduled date & time

    status = models.CharField(
        max_length=20,
        choices=[("Scheduled", "Scheduled"),
                 ("Completed", "Completed"),
                 ("Cancelled", "Cancelled"),
                 ("No-show", "No-show")],
        default="Scheduled"
    )
    notes = models.TextField(blank=True, null=True)    # Extra notes by doctor/admin

    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.patient} with {self.doctor}"

# Drug Table

class Drug(models.Model):
    drug_code = models.CharField(max_length=20, unique=True)
    drug_name = models.CharField(max_length=100)
    standard_dosage = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.drug_name} ({self.drug_code})"


# Prescription Table
class Prescription(models.Model):
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )
    visit = models.ForeignKey(
        "Visit",
        on_delete=models.CASCADE,
        related_name="prescriptions",
        null=True, blank=True
    )
  
    
    drug = models.ForeignKey(
        "Drug",
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )
    dosage = models.CharField(max_length=50)     # e.g., "500mg", can override standard
    FREQUENCY_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly')
    ]
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='Daily')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.drug.drug_name} for {self.patient.full_name} ({self.dosage}, {self.frequency})"


# Emergency Table
class Emergency(models.Model):
    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        related_name="emergencies"
    )
    critical_notes = models.TextField(blank=True, null=True)
    DNR_CHOICES = [
        ("yes", "Yes"),
        ("no", "No")
    ]
    dnr = models.CharField(max_length=3, choices=DNR_CHOICES, default="no")
    blood_group = models.CharField(max_length=3, blank=True, null=True)
    chronic_conditions = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    prescriptions_section = models.TextField(blank=True, null=True)
         


# Symptom Table
class Symptom(models.Model):
    symptom_code = models.CharField(max_length=20, unique=True)  # e.g., "FVR" for Fever
    name = models.CharField(max_length=100)                      # e.g., "Fever"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.symptom_code})"

# VisitSymptom Table
class VisitSymptom(models.Model):
    visit = models.ForeignKey("Visit", on_delete=models.CASCADE, related_name="visit_symptoms")
    symptom = models.ForeignKey("Symptom", on_delete=models.CASCADE)
    severity = models.CharField(max_length=10, choices=[('Mild', 'Mild'), ('Moderate', 'Moderate'), ('Severe', 'Severe')], default='Mild')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.symptom.name} ({self.severity}) for Visit {self.visit.visit_id}"

# Lifestyle Table
class Lifestyle(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="lifestyles")

    YES_NO_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
    ]

    smoking = models.CharField(max_length=3, choices=YES_NO_CHOICES)

    physical_activity = models.CharField(max_length=10, choices=[
        ("low", "Low"),
        ("moderate", "Moderate"),
        ("high", "High"),
    ])

    diabetes_in_family = models.CharField(max_length=3, choices=YES_NO_CHOICES, default="no")

    created_at = models.DateTimeField(auto_now_add=True)


