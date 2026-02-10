from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorData(BaseModel):
    user_id: str
    timestamp: Optional[datetime] = None
    cortisol_level: float  # µg/dL
    hrv: float            # ms
    eda: float            # µS
    screen_time_minutes: int

class PredictionResponse(BaseModel):
    user_id: str
    risk_score: float  # 0.0 to 1.0
    risk_level: str    # Low, Medium, High
    intervention: Optional[str] = None
    timestamp: datetime

class SurveyData(BaseModel):
    anxiety_level: int
    mental_health_history: int
    depression: int
    headache: int
    sleep_quality: int
    breathing_problem: int
    living_conditions: int
    academic_performance: int
    study_load: int
    future_career_concerns: int
    extracurricular_activities: int

class BiologicalData(BaseModel):
    hr: float
    eda: float
    temp: float

class TherapySessionInput(BaseModel):
    responses: list[str]
