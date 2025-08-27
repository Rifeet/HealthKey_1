from django.db import models



# Doctor Table.
class Doctor(models.Model):
    national_id = models.CharField(max_length=20, unique=True)  # Added national ID
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # store plain first
    email = models.EmailField(unique=True)
    specialist = models.CharField(max_length=100)

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
    mobile_number = models.CharField(max_length=15)
    allergies = models.TextField(blank=True, null=True)  # optional field
    
    def __str__(self):
        return f"{self.full_name} ({self.national_id})"