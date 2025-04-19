from typing import List, Dict, Any

class SymptomCheckerAgent:
    def check(self, symptoms: List[str]) -> Dict[str, Any]:
        urgent_symptoms = {"chest pain", "shortness of breath", "loss of consciousness", "convulsions", "confusion"}
        urgent = any(s in urgent_symptoms for s in symptoms)
        return {
            "urgent": urgent,
            "message": "Seek urgent/emergency care!" if urgent else "Monitor symptoms and consult a doctor if they worsen."
        }

if __name__ == "__main__":
    agent = SymptomCheckerAgent()
    print(agent.check(["fever", "chest pain"]))
