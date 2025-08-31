from django.urls import path
from . import views
from .views import patient_prediction_view

urlpatterns = [
    path("predict/", views.predict_view, name="predict"),
    path('predict/<int:patient_id>/', patient_prediction_view, name='patient_prediction'),
]