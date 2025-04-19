from typing import List, Dict, Any
import pandas as pd
import os
from .symptom_utils import fuzzy_match_symptoms

data_path = os.path.join(os.path.dirname(__file__), '../../data/mock_medical_data.csv')

class DiagnosisAgent:
    def __init__(self):
        self.df = pd.read_csv(data_path)
        self.known_symptoms = list(set(self.df['symptom'].str.lower().str.strip()))

    def diagnose(self, symptoms: List[str]) -> List[Dict[str, Any]]:
        # Emergency logic: prioritize neuro diagnoses if red flag symptoms
        neuro_red_flags = {"convulsions", "loss of consciousness", "confusion"}
        if any(s in neuro_red_flags for s in symptoms):
            # Hardcode top neuro diagnoses for safety
            neuro_diagnoses = [
                {"disease": "Seizure", "count": 1},
                {"disease": "Epilepsy", "count": 1},
                {"disease": "Post-ictal state", "count": 1}
            ]
            return neuro_diagnoses
        matched = fuzzy_match_symptoms(symptoms, self.known_symptoms, threshold=80)
        matches = self.df[self.df['symptom'].isin(matched)]
        diagnosis = matches['disease'].value_counts().head(3)
        return [{"disease": d, "count": int(c)} for d, c in diagnosis.items()]

if __name__ == "__main__":
    agent = DiagnosisAgent()
    print(agent.diagnose(["fever", "cough"]))
