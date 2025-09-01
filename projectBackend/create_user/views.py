from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Doctor, Patient, Visit, Symptom, VisitSymptom,Diagnosis, Disease, LabTest, Drug, Prescription,LabTestResult
from datetime import date
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


# Utility to calculate patient age
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # fetch doctor
            try:
                doctor = Doctor.objects.get(user=user)
                request.session['doctor_id'] = doctor.id  # store in session
            except Doctor.DoesNotExist:
                messages.error(request, "Doctor profile not found.")
                return redirect("login")

            return redirect("doctor_home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "create_user/login.html")


@login_required
def doctor_home(request):
    # fetch doctor using session or user
    doctor = get_object_or_404(Doctor, user=request.user)
    visit = None
    patient = None
    visit_created = False

    if request.method == "POST":
        patient_input = request.POST.get("patient_input")
        patient = Patient.objects.filter(national_id=patient_input).first()
        if not patient:
            patient = Patient.objects.filter(id=patient_input).first()

        if patient:
            visit = Visit.objects.create(
                patient=patient,
                doctor=doctor,
                hospital=doctor.hospital
            )
            visit_created = True
        else:
            messages.error(request, "Patient not found")
            

    context = {
        "doctor": doctor,
        "visit_created": visit_created,
        "visit": visit,
        "visit_id": visit.visit_id if visit_created else None,
        "patient_name": patient.full_name if patient else "",
        "patient_national_id": patient.national_id if patient else "",
        "patient_age": calculate_age(patient.dob) if patient else "",
        "symptoms": Symptom.objects.all(),
        "diseases": Disease.objects.all(),
        "lab_tests": LabTest.objects.all(),
        "drugs": Drug.objects.all(),
    }
    return render(request, "create_user/doctor_home.html", context)


@login_required
def save_visit_symptoms(request, visit_id):
    if request.method == "POST":
        visit = get_object_or_404(Visit, id=visit_id)
        try:
            data = json.loads(request.body)
            symptoms_list = data.get("symptoms", [])
            for s in symptoms_list:
                symptom = get_object_or_404(Symptom, id=s["symptom_id"])
                VisitSymptom.objects.create(
                    visit=visit,
                    symptom=symptom,
                    severity=s.get("severity", "Mild")
                )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method"})
@login_required
def save_diagnoses(request, visit_id):
    if request.method == "POST":
        visit = get_object_or_404(Visit, id=visit_id)

        # Expecting multiple diagnoses
        diseases_ids = request.POST.getlist("disease_ids[]")
        severities = request.POST.getlist("severities[]")
        notes_list = request.POST.getlist("notes[]")

        for i, disease_id in enumerate(diseases_ids):
            try:
                disease = Disease.objects.get(id=disease_id)
                severity = severities[i] if i < len(severities) else 'Mild'
                notes = notes_list[i] if i < len(notes_list) else ''
                Diagnosis.objects.create(
                    visit=visit,
                    disease=disease,
                    severity=severity,
                    notes=notes
                )
            except Disease.DoesNotExist:
                continue  # skip invalid disease IDs

        return JsonResponse({"success": True, "message": "Diagnoses saved successfully!"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

# Save Lab Test Results
@login_required
def save_lab_results(request, visit_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lab_results = data.get("lab_results", [])
            visit = Visit.objects.get(visit_id=visit_id)
            patient = visit.patient

            for item in lab_results:
                lab_test = LabTest.objects.get(id=item["lab_test_id"])
                LabTestResult.objects.create(
                    patient=patient,
                    visit=visit,
                    lab_test=lab_test,
                    result_value=item["result_value"],
                    notes=item.get("notes", "")
                )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

# Save Prescriptions
@login_required
def save_prescriptions(request, visit_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prescriptions_data = data.get("prescriptions", [])
            visit = Visit.objects.get(visit_id=visit_id)
            patient = visit.patient

            for item in prescriptions_data:
                drug = Drug.objects.get(id=item["drug_id"])
                Prescription.objects.create(
                    patient=patient,
                    visit=visit,
                    drug=drug,
                    dosage=item["dosage"],
                    frequency=item["frequency"],
                    notes=item.get("notes", "")
                )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from .models import Visit, Symptom, VisitSymptom, Diagnosis, Disease, LabTest, LabTestResult, Drug, Prescription

def save_all_data(request, visit_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method."})

    try:
        visit = get_object_or_404(Visit, visit_id=visit_id)
        data = json.loads(request.body)

        # --- Save Symptoms ---
        symptoms = data.get("symptoms", [])
        for s in symptoms:
            symptom = Symptom.objects.get(pk=s["symptom_id"])
            # Avoid duplicate VisitSymptom
            if not VisitSymptom.objects.filter(visit=visit, symptom=symptom).exists():
                VisitSymptom.objects.create(
                    visit=visit,
                    symptom=symptom,
                    severity=s.get("severity", "Mild"),
                    notes=s.get("notes", "")
                )

        # --- Save Diagnoses ---
        diagnoses = data.get("diagnoses", [])
        for d in diagnoses:
            disease = Disease.objects.get(pk=d["disease_id"])
            if not Diagnosis.objects.filter(visit=visit, disease=disease).exists():
                Diagnosis.objects.create(
                    visit=visit,
                    disease=disease,
                    severity=d.get("severity", "Mild"),
                    notes=d.get("notes", "")
                )

        # --- Save Lab Test Results ---
        lab_tests = data.get("lab_tests", [])
        for l in lab_tests:
            lab_test = LabTest.objects.get(pk=l["lab_test_id"])
            if not LabTestResult.objects.filter(visit=visit, lab_test=lab_test).exists():
                LabTestResult.objects.create(
                    patient=visit.patient,
                    visit=visit,
                    lab_test=lab_test,
                    result_value=l.get("result_value", ""),
                    notes=l.get("notes", "")
                )

        # --- Save Prescriptions ---
        prescriptions = data.get("prescriptions", [])
        for p in prescriptions:
            drug = Drug.objects.get(pk=p["drug_id"])
            if not Prescription.objects.filter(visit=visit, drug=drug).exists():
                Prescription.objects.create(
                    patient=visit.patient,
                    visit=visit,
                    drug=drug,
                    dosage=p.get("dosage", ""),
                    frequency=p.get("frequency", "Daily"),
                    notes=p.get("notes", "")
                )

        # Success response
        return JsonResponse({
            "success": True,
            "message": "All data saved successfully! Redirecting to login...",
            "redirect_url": "/login/"
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
