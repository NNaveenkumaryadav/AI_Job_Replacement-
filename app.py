from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

# Load trained model
model = joblib.load("model.joblib")

app = FastAPI(title="AI Job Replacement Prediction API")

# Enable CORS for the UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobInput(BaseModel):
    job_role: str
    industry: str
    country: str
    year: int
    automation_risk_percent: float
    skill_gap_index: float
    salary_before_usd: float
    salary_after_usd: float
    salary_change_percent: float
    skill_demand_growth_percent: float
    remote_feasibility_score: float
    ai_adoption_level: float
    education_requirement_level: int

@app.get("/")
def home():
    return {"message": "API is online 🚀"}

@app.post("/predict")
def predict(data: JobInput):
    input_df = pd.DataFrame([data.dict()])
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    return {
        "prediction": prediction,
        "class_probabilities": {
            model.classes_[i]: float(probabilities[i])
            for i in range(len(model.classes_))
        }
    }