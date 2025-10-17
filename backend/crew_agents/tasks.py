from crewai import Task
from .agents import symptom_analyzer, diagnosis_agent, routing_agent, report_agent

def create_symptom_analysis_task(symptoms: str, medical_context: str) -> Task:
    return Task(
        description=f"""
        Analyze the following patient symptoms and medical context:
        
        PATIENT SYMPTOMS: {symptoms}
        
        MEDICAL CONTEXT: {medical_context}
        
        Your task:
        1. Identify key symptoms and their severity
        2. Note any concerning or emergency indicators
        3. Provide initial medical assessment
        
        Output format:
        KEY_SYMPTOMS: [list of main symptoms]
        SEVERITY: [mild/moderate/severe/emergency]
        INITIAL_ASSESSMENT: [your medical assessment]
        """,
        agent=symptom_analyzer,
        expected_output="Structured symptom analysis with key findings and severity assessment"
    )

def create_diagnosis_task() -> Task:
    return Task(
        description="""
        Based on the symptom analysis, determine:
        
        1. Most likely medical condition(s)
        2. Recommended hospital department
        3. Urgency level
        4. Additional considerations
        
        Output format:
        CONDITION: [most likely condition]
        DEPARTMENT: [recommended department]
        URGENCY: [low/medium/high/emergency]
        CONSIDERATIONS: [additional medical considerations]
        """,
        agent=diagnosis_agent,
        expected_output="Medical diagnosis with department recommendation and urgency assessment"
    )

def create_routing_task(hospitals_data: str) -> Task:
    return Task(
        description=f"""
        Based on the diagnosis and department recommendation, find the best hospital match:
        
        AVAILABLE HOSPITALS: {hospitals_data}
        
        Your task:
        1. Match the recommended department with available hospitals
        2. Consider location and specialization
        3. Provide hospital recommendation
        
        Output format:
        RECOMMENDED_HOSPITAL: [hospital name and location]
        REASONING: [why this hospital is recommended]
        """,
        agent=routing_agent,
        expected_output="Hospital recommendation with clear reasoning"
    )

def create_report_task() -> Task:
    return Task(
        description="""
        Create a comprehensive triage report by synthesizing all previous analysis:
        
        Your task:
        1. Summarize the medical condition
        2. Provide clear department recommendation  
        3. Include hospital suggestion
        4. Give patient-friendly explanation
        
        Output format:
        FINAL_DIAGNOSIS: [clear condition summary]
        DEPARTMENT: [recommended department]
        HOSPITAL: [recommended hospital]
        PATIENT_EXPLANATION: [clear explanation for patient]
        """,
        agent=report_agent,
        expected_output="Complete triage report with patient-friendly recommendations"
    )