from django.urls import path
from . import views
from api.views import add_report
from .views import ReportListAPIView

urlpatterns = [
    path('hello/', views.say_hello),
    path('fetch-data/', views.fetch_data_view, name='fetch_data'),
    path('insert-data/', views.insert_data_view, name='insert_data'),
    path('add-report/', views.add_report, name='add_report'),
    path('reports/', ReportListAPIView.as_view(), name='api_reports'),
]
