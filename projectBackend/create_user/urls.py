from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.custom_login, name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("doctor-home/", views.doctor_home, name="doctor_home"),
    path("save-symptoms/<int:visit_id>/", views.save_visit_symptoms, name="save_visit_symptoms"),
    path("save-diagnoses/<int:visit_id>/", views.save_diagnoses, name="save_diagnoses"),
    path('save-lab-results/<int:visit_id>/', views.save_lab_results, name='save_lab_results'),
    path('save-prescriptions/<int:visit_id>/', views.save_prescriptions, name='save_prescriptions'),
    path('save-all-data/<int:visit_id>/', views.save_all_data, name='save_all_data'),
    path("login/", views.custom_login, name="login"),
]
