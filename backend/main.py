from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from typing import List, Dict
from gemini_service import gemini_service
from rag.retriever import medical_retriever
from crew_agents.crew import medical_crew

app = FastAPI(title="Healthcare AI Triage Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SymptomRequest(BaseModel):
    symptoms: str

class TriageResponse(BaseModel):
    diagnosis: str
    department: str
    hospital: str
    reasoning: str

class CrewTriageResponse(BaseModel):
    diagnosis: str
    department: str
    hospital: str
    reasoning: str
    workflow: str
    agents_used: int

class Hospital(BaseModel):
    name: str
    department: str
    location: str


def load_hospitals() -> List[Dict]:
    try:
        with open("data/hospitals.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


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
    relevant_context = medical_retriever.retrieve_context(request.symptoms, k=5)
    
    return {
        "query": request.symptoms,
        "relevant_knowledge": relevant_context,
        "total_matches": len(relevant_context),
        "method": "vector_search"
    }

@app.post("/analyze", response_model=TriageResponse)
async def analyze_symptoms(request: SymptomRequest):
    
    relevant_context = medical_retriever.retrieve_context(request.symptoms, k=3)
    
    analysis = gemini_service.analyze_symptoms(request.symptoms, relevant_context)
    
    hospitals = load_hospitals()
    recommended_hospital = "General Hospital"
    
    for hospital in hospitals:
        if analysis["department"].lower() in hospital["department"].lower():
            recommended_hospital = f"{hospital['name']} ({hospital['location']})"
            break
    
    return TriageResponse(
        diagnosis=analysis["condition"],
        department=analysis["department"],
        hospital=recommended_hospital,
        reasoning=analysis["reasoning"]
    )

@app.post("/analyze-crew", response_model=CrewTriageResponse)
async def analyze_symptoms_crew(request: SymptomRequest):
    hospitals = load_hospitals()
    
    analysis = medical_crew.analyze_symptoms(request.symptoms, hospitals)
    
    recommended_hospital = "General Hospital"
    
    for hospital in hospitals:
        if analysis["department"].lower() in hospital["department"].lower():
            recommended_hospital = f"{hospital['name']} ({hospital['location']})"
            break
    
    return CrewTriageResponse(
        diagnosis=analysis["condition"],
        department=analysis["department"],
        hospital=recommended_hospital,
        reasoning=analysis["reasoning"],
        workflow="CrewAI Multi-Agent Sequential",
        agents_used=4
    )

@app.get("/health")
async def health_check():
    hospitals_count = len(load_hospitals())
    knowledge_lines = len(load_medical_knowledge().split('\n'))
    rag_status = medical_retriever.get_status()
    crew_status = medical_crew.get_workflow_status()
    
    return {
        "status": "healthy", 
        "feature": "Feature 5 - CrewAI Multi-Agent System",
        "hospitals_loaded": hospitals_count,
        "knowledge_entries": knowledge_lines,
        "vector_index_loaded": rag_status["index_loaded"],
        "vector_documents": rag_status["total_documents"],
        "crew_agents": crew_status["agents_count"],
        "workflow_type": crew_status["workflow_type"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)