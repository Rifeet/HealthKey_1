from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .forms import PatientForm
from ai_engine.models import PatientFeatures
from ai_engine.prediction import predict_patient
from .prediction import predict_patient
from .db_prediction import predict_patient

def run_prediction(request, patient_id):
    result = predict_patient(patient_id)
    return HttpResponse(f"Prediction saved: {result}")

def predict_view(request):
    if request.method == "POST":
        patient_data = request.POST.dict()  # If form submission
        result = predict_patient(patient_data)
        return JsonResponse(result)

    return JsonResponse({"error": "Only POST allowed"})



def patient_predict_view(request):
    result = None

    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient_data = form.cleaned_data
            result = predict_patient(patient_data)
    else:
        form = PatientForm()

    return render(request, "ai_engine/patient_form.html", {"form": form, "result": result})

def predict_view(request):
    result = None

    if request.method == "POST":
        patient_data = { key: request.POST.get(key) for key in [
            "patient_id","age","gender","BMI","smoking","physical_activity",
            "glucose","HbA1c","cholesterol","blood_pressure_systolic",
            "blood_pressure_diastolic","creatinine","microalbuminuria",
            "c_peptide","diabetes_in_family","previous_diagnoses","drug_history"
        ]}
        result = predict_patient(patient_data)

    # Always render the template with result (None if GET)
    return render(request, "ai_engine/predict_form.html", {"result": result})

def patient_prediction_view(request, patient_id):
    try:
        pf = PatientFeatures.objects.get(patient_id=patient_id)
        patient_data = {
            "patient_id": pf.patient.id,
            "age": pf.age,
            "gender": pf.gender,
            "BMI": pf.BMI,
            "smoking": pf.smoking,
            "physical_activity": pf.physical_activity,
            "glucose": pf.glucose,
            "HbA1c": pf.HbA1c,
            "cholesterol": pf.cholesterol,
            "blood_pressure_systolic": pf.blood_pressure_systolic,
            "blood_pressure_diastolic": pf.blood_pressure_diastolic,
            "creatinine": pf.creatinine,
            "microalbuminuria": pf.microalbuminuria,
            "c_peptide": pf.c_peptide,
            "diabetes_in_family": pf.diabetes_in_family,
            "previous_diagnoses": pf.previous_diagnoses,
            "drug_history": pf.drug_history
        }
        prediction = predict_patient(patient_data)
    except PatientFeatures.DoesNotExist:
        prediction = {"error": "Patient not found"}

    return render(request, "ai_engine/prediction_result.html", {"prediction": prediction})