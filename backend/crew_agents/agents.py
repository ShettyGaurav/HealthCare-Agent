from crewai import Agent
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class CrewAIGeminiWrapper:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY is required for CrewAI agents")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.model_name = "gemini-2.5-flash"
    
    def call(self, prompt, **kwargs):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def __call__(self, prompt, **kwargs):
        return self.call(prompt, **kwargs)

def get_gemini_llm():
    return CrewAIGeminiWrapper()

llm = get_gemini_llm()

try:
    symptom_analyzer = Agent(
        role="Medical Symptom Analyzer",
        goal="Analyze and interpret patient symptoms with medical context",
        backstory="""You are an experienced medical professional specializing in symptom analysis. 
        You excel at understanding patient descriptions and identifying key medical indicators.""",
        verbose=False,
        allow_delegation=False
    )

    diagnosis_agent = Agent(
        role="Medical Diagnosis Specialist",
        goal="Determine most likely medical conditions and required departments",
        backstory="""You are a senior diagnostician with expertise in differential diagnosis. 
        You analyze symptoms and medical context to identify probable conditions and specialist requirements.""",
        verbose=False,
        allow_delegation=False
    )

    routing_agent = Agent(
        role="Hospital Routing Specialist", 
        goal="Match patients with appropriate hospitals and departments",
        backstory="""You are a healthcare coordinator who knows hospital capabilities and specialties. 
        You excel at matching patient needs with the right medical facilities.""",
        verbose=False,
        allow_delegation=False
    )

    report_agent = Agent(
        role="Medical Report Generator",
        goal="Create comprehensive triage reports with clear recommendations",
        backstory="""You are a medical documentation specialist who creates clear, actionable reports. 
        You synthesize medical analysis into professional recommendations for patients and healthcare providers.""",
        verbose=False,
        allow_delegation=False
    )
except Exception as e:
    print(f"CrewAI Agent creation failed: {e}")
    symptom_analyzer = None
    diagnosis_agent = None
    routing_agent = None
    report_agent = None