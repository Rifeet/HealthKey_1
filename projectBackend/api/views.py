from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from authentication.supabase_client import SupabaseClient
from django.http import JsonResponse
from .models import Report
from .serializer import ReportSerializer
from .forms import ReportForm
from rest_framework import generics
from .supabase_utils import fetch_from_supabase, insert_to_supabase

def say_hello(request):
    return render(request, 'hello.html', {'name': 'Rifeet'}) 

def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/add_report/')
    else:
        form = ReportForm()
    return render(request, 'add_report.html', {'form': form})

class ReportListAPIView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

def fetch_data_view(request):
    data = fetch_from_supabase('your_table_name')
    return JsonResponse(data, safe=False)

def insert_data_view(request):
    if request.method == 'POST':
        data = request.POST.dict()
        response = insert_to_supabase('your_table_name', data)
        return JsonResponse(response, safe=False)       
    
