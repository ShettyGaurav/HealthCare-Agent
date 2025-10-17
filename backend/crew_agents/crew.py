from crewai import Crew, Process
from .agents import symptom_analyzer, diagnosis_agent, routing_agent, report_agent
from .tasks import create_symptom_analysis_task, create_diagnosis_task, create_routing_task, create_report_task
from rag.retriever import medical_retriever
import json

class MedicalTriageCrew:
    def __init__(self):
        self.crew = None
        
    def analyze_symptoms(self, symptoms: str, hospitals_data: list) -> dict:
        
        medical_context = medical_retriever.retrieve_context(symptoms, k=3)
        context_str = "\n".join(medical_context) if medical_context else "No specific medical context found"
        
        hospitals_str = json.dumps(hospitals_data[:10], indent=2)
        
        tasks = [
            create_symptom_analysis_task(symptoms, context_str),
            create_diagnosis_task(),
            create_routing_task(hospitals_str),
            create_report_task()
        ]
        

        self.crew = Crew(
            agents=[symptom_analyzer, diagnosis_agent, routing_agent, report_agent],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        

        try:
            result = self.crew.kickoff()
            return self._parse_crew_result(result)
        except Exception as e:
            print(f"CrewAI execution error: {e}")
            return self._fallback_analysis(symptoms)
    
    def _parse_crew_result(self, result: str) -> dict:
        lines = result.strip().split('\n')
        
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
            "crew_initialized": self.crew is not None,
            "agents_count": 4,
            "workflow_type": "sequential"
        }


medical_crew = MedicalTriageCrew()