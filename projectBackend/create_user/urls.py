from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.hello, name='hello'), # test view
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('doctor-success/', views.doctor_success, name='doctor_success'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('patient-success/', views.patient_success, name='patient_success'),
]