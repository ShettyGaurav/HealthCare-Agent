import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError(
                "GEMINI_API_KEY is required. Please set it in your .env file."
            )

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        print("SUCCESS: Gemini AI initialized successfully")

    def analyze_symptoms(self, symptoms: str, medical_context: List[str]) -> Dict:

        context = "\n".join(medical_context[:3]) if medical_context else ""

        prompt = f"""
You are a medical triage assistant. Analyze the following symptoms and provide a structured response.

SYMPTOMS: {symptoms}

MEDICAL CONTEXT:
{context}

Please provide:
1. Most likely medical condition
2. Recommended hospital department
3. Brief reasoning (2-3 sentences)

Format your response as:
CONDITION: [condition name]
DEPARTMENT: [department name]  
REASONING: [your reasoning]
"""

        response = self.model.generate_content(prompt)
        return self._parse_gemini_response(response.text)

    def _parse_gemini_response(self, response_text: str) -> Dict:
        lines = response_text.strip().split("\n")

        condition = "General medical condition"
        department = "General Medicine"
        reasoning = "AI analysis completed"

        for line in lines:
            if line.startswith("CONDITION:"):
                condition = line.replace("CONDITION:", "").strip()
            elif line.startswith("DEPARTMENT:"):
                department = line.replace("DEPARTMENT:", "").strip()
            elif line.startswith("REASONING:"):
                reasoning = line.replace("REASONING:", "").strip()

        return {
            "condition": condition,
            "department": department,
            "reasoning": reasoning,
        }


gemini_service = GeminiService()
