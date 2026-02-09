from ..backend.models import SensorData, PredictionResponse
from datetime import datetime

def calculate_risk(data: SensorData) -> PredictionResponse:
    # --- SIMULATED AI LOGIC ---
    # Normal Ranges:
    # Cortisol: 6-23 µg/dL (Morning), <10 (Evening). Let's say >20 is high stress.
    # HRV: >50ms is good. <30ms is stress.
    
    score = 0.0
    
    # 1. Cortisol Factor (Weight: 40%)
    if data.cortisol_level > 20:
        score += 0.4
    elif data.cortisol_level > 15:
        score += 0.2
        
    # 2. HRV Factor (Weight: 30%)
    if data.hrv < 30:
        score += 0.3
    elif data.hrv < 50:
        score += 0.15
        
    # 3. Screen Time Factor (Weight: 30%)
    # If high stress + high screen time = PROCRASTINATION
    if data.screen_time_minutes > 60:
        score += 0.3
    elif data.screen_time_minutes > 30:
        score += 0.15
        
    # Classification
    if score >= 0.7:
        risk_level = "High"
        intervention = "LOCK_SOCIAL_MEDIA"
    elif score >= 0.4:
        risk_level = "Medium"
        intervention = "TAKE_A_BREATH"
    else:
        risk_level = "Low"
        intervention = None
        
    return PredictionResponse(
        user_id=data.user_id,
        risk_score=round(score, 2),
        risk_level=risk_level,
        intervention=intervention,
        timestamp=datetime.now()
    )
