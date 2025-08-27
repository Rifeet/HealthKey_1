from django.shortcuts import render, redirect
from .forms import DoctorForm, PatientForm

def hello(request):
    return render(request, 'create_user/hello.html')


def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()  # saves data to the database
            return redirect('doctor_success')  # redirect after saving
    else:
        form = DoctorForm()
    return render(request, 'create_user/add_doctor.html', {'form': form})

def doctor_success(request):
    return render(request, 'create_user/doctor_success.html')

## patient views 
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_success')
    else:
        form = PatientForm()
    return render(request, 'create_user/add_patient.html', {'form': form})

def patient_success(request):
    return render(request, 'create_user/patient_success.html')