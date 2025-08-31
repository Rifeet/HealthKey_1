# ai_engine/prediction.py
import pandas as pd
import joblib
import networkx as nx
import os

# __file__ = path of this current file (prediction.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_diabetes_model2.pkl")
GRAPH_PATH = os.path.join(BASE_DIR, "models", "unified_knowledge_graph1.graphml")
PATIENTS_PATH   = os.path.join(BASE_DIR, "models", "patients300.csv")
KG_FEATURES_PATH = os.path.join(BASE_DIR, "models", "kg_features2.csv")


# Load model at module import (so it doesn’t reload on every request)
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None
try:
    G = nx.read_graphml(GRAPH_PATH)
except FileNotFoundError:
    print(" Graph file not found.")
    G = None

try:
    df_patients = pd.read_csv(PATIENTS_PATH)
    print(f"✅ Patient data loaded: {df_patients.shape}")
except FileNotFoundError:
    df_patients = pd.DataFrame()

try:
    df_kg_features = pd.read_csv(KG_FEATURES_PATH)
    df_kg_features['patient_id'] = df_kg_features['patient_id'].astype(str)
    print(f"✅ KG embeddings loaded: {df_kg_features.shape}")
except FileNotFoundError:
    df_kg_features = pd.DataFrame()
    print("❌ KG embeddings file not found!")

def predict_patient(patient_data: dict):
    """
    Takes patient_data (dict from form),
    merges with KG embeddings, and returns prediction & recommendation.
    """
    if model is None:
        return {"error": "Model not loaded"}
    if df_kg_features.empty:
        return {"error": "KG embeddings not loaded"}

    # Convert form data to DataFrame
    df = pd.DataFrame([patient_data])
    df['patient_id'] = df['patient_id'].astype(str)

    # Merge with KG embeddings
    df_merged = pd.merge(df, df_kg_features, on='patient_id', how='left')
    df_merged.fillna(0, inplace=True)  # fill missing embeddings with 0

    # Prepare features for XGBoost
    target_column = 'label'  # not used here
    if 'patient_id' in df_merged.columns:
        df_merged.drop('patient_id', axis=1, inplace=True)

    # Convert categorical columns
    categorical_cols = ['gender', 'smoking', 'physical_activity',
                        'previous_diagnoses', 'drug_history',
                        'diabetes_in_family', 'microalbuminuria']
    for col in categorical_cols:
        if col in df_merged.columns:
            df_merged[col] = df_merged[col].astype('category')

    # Convert numeric columns to float
    numeric_cols = ['age', 'BMI', 'glucose', 'HbA1c', 'cholesterol',
                    'blood_pressure_systolic', 'blood_pressure_diastolic',
                    'creatinine', 'c_peptide']  # plus any embedding columns
    for col in numeric_cols:
        if col in df_merged.columns:
            df_merged[col] = pd.to_numeric(df_merged[col], errors='coerce')

    # Add degree_centrality and all embedding columns
    numeric_cols += ['degree_centrality']
    embedding_cols = [col for col in df_merged.columns if col.startswith("embedding_")]
    numeric_cols += embedding_cols

    for col in numeric_cols:
        if col in df_merged.columns:
            df_merged[col] = pd.to_numeric(df_merged[col], errors='coerce').fillna(0)        

    print(df_merged.head())
    print(df_merged.dtypes)
    # Predict
    prediction = model.predict(df_merged)[0]
    probability = model.predict_proba(df_merged)[:, 1][0]

    # Risk assessment
    if probability >= 0.8:
        risk_level = "Very High"
        recommendation = "Immediate medical consultation required"
    elif probability >= 0.6:
        risk_level = "High"
        recommendation = "Consult with a medical professional soon"
    elif probability >= 0.4:
        risk_level = "Moderate"
        recommendation = "Consider lifestyle changes and monitoring"
    else:
        risk_level = "Low"
        recommendation = "Maintain healthy lifestyle"

    return {
        "prediction": int(prediction),
        "probability": float(probability),
        "risk_level": risk_level,
        "recommendation": recommendation
    }