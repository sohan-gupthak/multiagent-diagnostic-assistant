from typing import List, Dict, Any

class DifferentialDiagnosisAgent:
    def __init__(self):
        # Simple mock differentials; in production, use a real knowledge base
        # can be optimized 
        self.differential_map = {
            "cough": ["Asthma", "Bronchitis", "Pneumonia", "Tuberculosis"],
            "chest pain": ["Angina", "Myocardial Infarction", "GERD", "Costochondritis"],
            "headache": ["Migraine", "Tension Headache", "Cluster Headache", "Meningitis"],
            "fever": ["Flu", "COVID-19", "Malaria", "UTI"]
        }

    def suggest_differentials(self, symptoms: List[str]) -> List[str]:
        differentials = set()
        for s in symptoms:
            for key, vals in self.differential_map.items():
                if key in s:
                    differentials.update(vals)
        return list(differentials)

if __name__ == "__main__":
    agent = DifferentialDiagnosisAgent()
    print(agent.suggest_differentials(["cough", "chest pain"]))
