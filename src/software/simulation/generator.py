import requests
import time
import random
import json
from datetime import datetime

API_URL = "http://localhost:8000/api/v1/ingest"
USER_ID = "student_01"

def generate_sensor_data():
    """Generates synthetic sensor data with a simulated stress event."""
    
    # Base values (Resting state)
    cortisol = 10.0
    hrv = 60.0
    eda = 2.0
    screen_time = 15
    
    print(f"Starting simulation for user: {USER_ID}")
    print("Press Ctrl+C to stop.")
    
    step = 0
    
    while True:
        try:
            # Simulate a "Stress Event" between step 20 and 40 (e.g., Deadline approaching)
            if 20 <= step % 60 <= 40:
                print("--- SIMULATING STRESS EVENT ---")
                cortisol += random.uniform(0.5, 2.0)
                hrv -= random.uniform(1.0, 3.0)
                eda += random.uniform(0.1, 0.5)
                screen_time += random.randint(1, 5) # Doomscrolling increases
            else:
                # Recovery
                cortisol = max(5.0, cortisol - 0.5)
                hrv = min(100.0, hrv + 1.0)
                eda = max(1.0, eda - 0.1)
                screen_time = max(0, screen_time - 1)

            # Add some random noise
            current_cortisol = round(cortisol + random.uniform(-1, 1), 2)
            current_hrv = round(hrv + random.uniform(-2, 2), 1)
            current_eda = round(eda + random.uniform(-0.1, 0.1), 2)
            
            payload = {
                "user_id": USER_ID,
                "cortisol_level": current_cortisol,
                "hrv": current_hrv,
                "eda": current_eda,
                "screen_time_minutes": int(screen_time),
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                print(f"Sent: Cortisol={current_cortisol}, HRV={current_hrv} -> Risk: {result['risk_level']} ({result['intervention']})")
            else:
                print(f"Error: {response.status_code}")
                
            step += 1
            time.sleep(2)  # Send data every 2 seconds
            
        except Exception as e:
            print(f"Connection Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    generate_sensor_data()
