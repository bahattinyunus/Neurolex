
import pandas as pd
import numpy as np
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Global model and encoder
_model = None
_encoder = None

def _load_and_train_model():
    global _model, _encoder
    
    # Path to the dataset
    dataset_path = os.path.join(os.path.dirname(__file__), "data", "StressLevelDataset.csv")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return

    # Load dataset
    data = pd.read_csv(dataset_path)
    
    _encoder = LabelEncoder()
    data["stress_level"] = _encoder.fit_transform(data["stress_level"])

    # Split dataset
    X = data.drop("stress_level", axis=1)
    y = data["stress_level"]

    # Train model
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    _model = DecisionTreeClassifier(max_depth=7, random_state=100)
    _model.fit(X, y)
    print("Survey Model Trained Successfully.")

def predict_survey_stress(inputs: list) -> str:
    """
    Predicts stress level based on survey inputs.
    inputs: [anxiety_level, mental_health_history, depression, headache, sleep_quality, 
             breathing_problem, living_conditions, academic_performance, study_load, 
             future_career_concerns, extracurricular_activities]
    """
    global _model, _encoder
    
    if _model is None:
        _load_and_train_model()
        
    if _model is None:
        return "Error: Model not loaded"

    try:
        # Convert inputs to numpy array
        user_input = np.array([inputs])
        
        # Predict
        predicted_index = _model.predict(user_input)[0]
        
        # Decode label
        predicted_label = _encoder.inverse_transform([predicted_index])[0]
        
        # Map to readable string if necessary, though the dataset usually has 0, 1, 2
        # Assuming the dataset usually has strings 'Low', 'Medium', 'High' or numbers.
        # Based on the source code, it returns a value that is then displayed.
        # Let's assume the encoder handles the classes present in the CSV.
        
        return str(predicted_label)
        
    except Exception as e:
        return f"Error: {str(e)}"

# Train on import if possible, or lazy load
# _load_and_train_model()
