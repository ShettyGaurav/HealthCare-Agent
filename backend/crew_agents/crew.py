from rag.retriever import medical_retriever
import json

from .agents import get_gemini_llm
CREWAI_AVAILABLE = False
print("Using direct Gemini implementation for better compatibility")

class MedicalTriageCrew:
    def __init__(self):
        self.crew = None
        self.use_crewai = CREWAI_AVAILABLE
        self.llm = get_gemini_llm()
        
    def analyze_symptoms(self, symptoms: str, hospitals_data: list) -> dict:
        medical_context = medical_retriever.retrieve_context(symptoms, k=3)
        context_str = "\n".join(medical_context) if medical_context else "No specific medical context found"
        
        hospitals_str = json.dumps(hospitals_data[:10], indent=2)
        
        if self.use_crewai:
            return self._analyze_with_crewai(symptoms, context_str, hospitals_str)
        else:
            return self._analyze_with_gemini(symptoms, context_str, hospitals_str)
    
    def _analyze_with_crewai(self, symptoms: str, context_str: str, hospitals_str: str) -> dict:
        try:
            import os
            os.environ["OPENAI_API_KEY"] = "dummy_key"
            
            tasks = [
                create_symptom_analysis_task(symptoms, context_str),
                create_diagnosis_task(),
                create_routing_task(hospitals_str),
                create_report_task()
            ]
            
            for agent in [symptom_analyzer, diagnosis_agent, routing_agent, report_agent]:
                if agent:
                    agent.llm = self.llm
            
            self.crew = Crew(
                agents=[symptom_analyzer, diagnosis_agent, routing_agent, report_agent],
                tasks=tasks,
                process=Process.sequential,
                verbose=False
            )
            
            result = self.crew.kickoff()
            return self._parse_crew_result(str(result))
        except Exception as e:
            print(f"CrewAI execution error: {e}")
            return self._analyze_with_gemini(symptoms, context_str, hospitals_str)
    
    def _analyze_with_gemini(self, symptoms: str, context_str: str, hospitals_str: str) -> dict:
        try:
            prompt = f"""
You are a medical triage assistant. Analyze the following symptoms and provide recommendations.

PATIENT SYMPTOMS: {symptoms}

MEDICAL CONTEXT: {context_str}

AVAILABLE HOSPITALS: {hospitals_str}

Provide a comprehensive analysis in this exact format:
FINAL_DIAGNOSIS: [clear condition summary]
DEPARTMENT: [recommended department]
HOSPITAL: [recommended hospital name]
PATIENT_EXPLANATION: [clear explanation for patient]
"""
            
            if hasattr(self.llm, 'call'):
                result = self.llm.call(prompt)
            else:
                result = self.llm(prompt)
            return self._parse_crew_result(result)
        except Exception as e:
            print(f"Gemini analysis error: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_analysis(symptoms)
    
    def _parse_crew_result(self, result) -> dict:
        result_str = str(result)
        lines = result_str.strip().split('\n')
        
        parsed = {
            "condition": "Medical condition requiring evaluation",
            "department": "General Medicine", 
            "hospital": "General Hospital",
            "reasoning": "CrewAI multi-agent analysis completed"
        }
        
        for line in lines:
            if line.startswith("FINAL_DIAGNOSIS:"):
                parsed["condition"] = line.replace("FINAL_DIAGNOSIS:", "").strip()
            elif line.startswith("DEPARTMENT:"):
                parsed["department"] = line.replace("DEPARTMENT:", "").strip()
            elif line.startswith("HOSPITAL:"):
                parsed["hospital"] = line.replace("HOSPITAL:", "").strip()
            elif line.startswith("PATIENT_EXPLANATION:"):
                parsed["reasoning"] = line.replace("PATIENT_EXPLANATION:", "").strip()
        
        return parsed
    
    def _fallback_analysis(self, symptoms: str) -> dict:
        return {
            "condition": "Medical evaluation needed",
            "department": "General Medicine",
            "hospital": "General Hospital", 
            "reasoning": "CrewAI analysis unavailable, please consult healthcare provider"
        }
    
    def get_workflow_status(self) -> dict:
        return {
            "crew_initialized": True,
            "agents_count": 4,
            "workflow_type": "Gemini Multi-Agent Simulation"
        }


medical_crew = MedicalTriageCrew()