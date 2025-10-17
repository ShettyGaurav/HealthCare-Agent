from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from typing import List, Dict

app = FastAPI(title="Healthcare AI Triage Assistant", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class SymptomRequest(BaseModel):
    symptoms: str

class TriageResponse(BaseModel):
    diagnosis: str
    department: str
    hospital: str
    reasoning: str

class Hospital(BaseModel):
    name: str
    department: str
    location: str

# Load hospital data
def load_hospitals() -> List[Dict]:
    try:
        with open("data/hospitals.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Load medical knowledge
def load_medical_knowledge() -> str:
    try:
        with open("data/medical_knowledge.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

@app.get("/")
async def root():
    return {"message": "Healthcare AI Assistant API", "status": "running"}

@app.get("/hospitals", response_model=List[Hospital])
async def get_hospitals():
    hospitals = load_hospitals()
    return hospitals

@app.post("/rag-query")
async def rag_query(request: SymptomRequest):
    """Query medical knowledge base (basic implementation)"""
    knowledge = load_medical_knowledge()
    symptoms = request.symptoms.lower()
    
    relevant_lines = []
    for line in knowledge.split('\n'):
        if any(symptom in line.lower() for symptom in symptoms.split()):
            relevant_lines.append(line)

    return {
        "query": symptoms,
        "relevant_knowledge": relevant_lines[:3],
        "total_matches": len(relevant_lines)
    }

@app.post("/analyze", response_model=TriageResponse)
async def analyze_symptoms(request: SymptomRequest):
    return TriageResponse(
        diagnosis="Basic analysis - Feature 1 test",
        department="General Medicine",
        hospital="Test Hospital",
        reasoning="This is a basic response for Feature 1 testing"
    )

@app.get("/health")
async def health_check():
    hospitals_count = len(load_hospitals())
    knowledge_lines = len(load_medical_knowledge().split('\n'))
    return {
        "status": "healthy", 
        "feature": "Feature 2 - Demo Data Setup",
        "hospitals_loaded": hospitals_count,
        "knowledge_entries": knowledge_lines
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)