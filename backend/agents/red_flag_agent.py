from typing import List, Dict, Any

class RedFlagAgent:
    def __init__(self):
        self.red_flags = [
            "sudden severe chest pain", "loss of consciousness", "hemoptysis", "severe shortness of breath", "stiff neck", "confusion", "seizure"
        ]

    def check_red_flags(self, user_input: str, symptoms: List[str]) -> List[str]:
        found = []
        for rf in self.red_flags:
            if rf in user_input.lower():
                found.append(rf)
        for s in symptoms:
            if s in self.red_flags:
                found.append(s)
        return found

if __name__ == "__main__":
    agent = RedFlagAgent()
    print(agent.check_red_flags("Patient had loss of consciousness and seizure", ["seizure"]))
