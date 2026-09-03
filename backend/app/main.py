from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import sys
import os
from contextlib import asynccontextmanager
from .schemas import PredictionRequest, PredictionResponse

# Ensure the custom FeatureEngineer class can be unpickled by joblib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.features.preprocessing import FeatureEngineer 

# Global state for the model
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    model_path = os.path.join(os.path.dirname(__file__), '../../models/final_defect_prediction_pipeline.joblib')
    try:
        ml_models["pipeline"] = joblib.load(model_path)
        ml_models["version"] = "LogisticRegression-Pipeline-v1"
        print(f"Model loaded successfully from {model_path}")
    except Exception as e:
        print(f"Failed to load model: {e}")
        ml_models["pipeline"] = None
    yield
    # Clean up
    ml_models.clear()

app = FastAPI(
    title="Semiconductor Quality Intelligence API",
    description="API for predicting manufacturing defects based on process telemetry and environmental conditions.",
    version="1.0.0",
    lifespan=lifespan
)

# Allow CORS for the dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
def health_check():
    model_loaded = ml_models.get("pipeline") is not None
    return {
        "status": "healthy",
        "model_loaded": model_loaded
    }

def get_risk_level(probability: float) -> str:
    if probability < 0.20:
        return "LOW"
    elif probability < 0.50:
        return "MEDIUM"
    else:
        return "HIGH"

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_defect(request: PredictionRequest):
    pipeline = ml_models.get("pipeline")
    if not pipeline:
        raise HTTPException(status_code=503, detail="Machine learning model is currently unavailable.")
    
    # Convert Pydantic object to Pandas DataFrame (single row)
    input_data = pd.DataFrame([request.model_dump()])
    
    try:
        # Perform inference
        prediction = pipeline.predict(input_data)[0]
        # Get probability of class '1' (Defective)
        probability = pipeline.predict_proba(input_data)[0][1]
        
        # Determine risk classification
        risk_level = get_risk_level(probability)
        
        return PredictionResponse(
            prediction=int(prediction),
            defect_probability=float(probability),
            risk_level=risk_level,
            model_version=ml_models.get("version", "unknown")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")
