import spacy
from typing import Dict, Any
from .symptom_utils import extract_medical_symptoms

nlp = spacy.load('en_core_web_sm')

class NLPAgent:
    def parse_input(self, user_input: str) -> Dict[str, Any]:
        """
        Extracts and normalizes medical symptoms from user input.
        """
        doc = nlp(user_input)
        symptoms = extract_medical_symptoms(user_input)
        return {"symptoms": symptoms, "raw": user_input}

if __name__ == "__main__":
    agent = NLPAgent()
    print(agent.parse_input("Patient reports fever, cough, and shortness of breath for 3 days."))
