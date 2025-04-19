from typing import List, Dict, Any

class ComorbidityAgent:
    def __init__(self):
        self.comorbidities = ["diabetes", "hypertension", "smoking", "asthma", "COPD", "cancer"]

    def extract_comorbidities(self, user_input: str) -> List[str]:
        found = []
        for c in self.comorbidities:
            if c in user_input.lower():
                found.append(c)
        return found

if __name__ == "__main__":
    agent = ComorbidityAgent()
    print(agent.extract_comorbidities("History of diabetes and smoking."))
