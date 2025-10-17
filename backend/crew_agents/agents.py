from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()


def get_gemini_llm():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is required for CrewAI agents")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.3
    )

llm = get_gemini_llm()


symptom_analyzer = Agent(
    role="Medical Symptom Analyzer",
    goal="Analyze and interpret patient symptoms with medical context",
    backstory="""You are an experienced medical professional specializing in symptom analysis. 
    You excel at understanding patient descriptions and identifying key medical indicators.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

  
diagnosis_agent = Agent(
    role="Medical Diagnosis Specialist",
    goal="Determine most likely medical conditions and required departments",
    backstory="""You are a senior diagnostician with expertise in differential diagnosis. 
    You analyze symptoms and medical context to identify probable conditions and specialist requirements.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)


routing_agent = Agent(
    role="Hospital Routing Specialist", 
    goal="Match patients with appropriate hospitals and departments",
    backstory="""You are a healthcare coordinator who knows hospital capabilities and specialties. 
    You excel at matching patient needs with the right medical facilities.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)


report_agent = Agent(
    role="Medical Report Generator",
    goal="Create comprehensive triage reports with clear recommendations",
    backstory="""You are a medical documentation specialist who creates clear, actionable reports. 
    You synthesize medical analysis into professional recommendations for patients and healthcare providers.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)