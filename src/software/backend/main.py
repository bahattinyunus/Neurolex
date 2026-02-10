from fastapi import FastAPI, HTTPException
from .models import SensorData, PredictionResponse, SurveyData, BiologicalData, TherapySessionInput
from ..ai.risk_engine import calculate_risk
from ..ai.survey_model import predict_survey_stress
from ..ai.biological_model import predict_biological_stress
from ..ai.therapist import TherapeuticAssistant
from datetime import datetime

app = FastAPI(title="Neurolex API", version="0.1.0")

# In-memory storage for MVP (simulate database)
sensor_log = []

@app.get("/")
def read_root():
    return {"status": "active", "system": "Neurolex MVP"}

@app.post("/api/v1/ingest", response_model=PredictionResponse)
def ingest_data(data: SensorData):
    # Add timestamp if missing
    if not data.timestamp:
        data.timestamp = datetime.now()
    
    # Store raw data
    sensor_log.append(data)
    
    # Calculate Risk
    risk_result = calculate_risk(data)
    
    return risk_result

@app.get("/api/v1/history")
def get_history(limit: int = 100):
    return sensor_log[-limit:]

@app.post("/api/v1/predict/survey")
def predict_survey(data: SurveyData):
    inputs = [
        data.anxiety_level, data.mental_health_history, data.depression,
        data.headache, data.sleep_quality, data.breathing_problem,
        data.living_conditions, data.academic_performance, data.study_load,
        data.future_career_concerns, data.extracurricular_activities
    ]
    result = predict_survey_stress(inputs)
    return {"stress_level": result}

@app.post("/api/v1/predict/biological")
def predict_biological(data: BiologicalData):
    score, label = predict_biological_stress(data.hr, data.eda, data.temp)
    return {"risk_score": score, "risk_label": label}

@app.post("/api/v1/therapist/process")
def process_therapy_session(data: TherapySessionInput):
    return TherapeuticAssistant.process_session(data.responses)
