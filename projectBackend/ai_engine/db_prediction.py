# db_prediction.py

import os
import joblib
from django.shortcuts import get_object_or_404
from .models import Patient, PredictionResult

# Load trained model once (on server start)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_diabetes_model2.pkl")
model = joblib.load(MODEL_PATH)


def predict_patient(patient_id):
    """
    Predict diabetes risk for a given patient, save it in PredictionResult, 
    and return the saved result.
    """
    # 1. Get the patient object
    patient = get_object_or_404(Patient, id=patient_id)

    # 2. Extract features from patient (example: adjust based on your Patient model fields)
    features = [
        patient.age,
        patient.bmi,
        patient.glucose_level,
        patient.blood_pressure,
        patient.insulin,
        patient.skin_thickness,
        patient.pregnancies,
    ]

    # 3. Run prediction
    prediction_proba = model.predict_proba([features])[0]
    prediction = int(prediction_proba[1] >= 0.5)  # 1 = Diabetic, 0 = Healthy
    probability = float(round(prediction_proba[1], 2))

    # 4. Risk level & recommendation
    if prediction == 0:
        risk_level = "Low Risk"
        recommendation = "Maintain a healthy lifestyle with regular exercise and a balanced diet."
    else:
        risk_level = "High Risk"
        recommendation = "Consult a doctor for further tests and adopt a strict diet and exercise plan."

    # 5. Save result in DB
    result = PredictionResult.objects.create(
        patient=patient,
        prediction=prediction,
        probability=probability,
        risk_level=risk_level,
        recommendation=recommendation,
    )

    return result  # Returns the saved object
