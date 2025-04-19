from typing import List, Dict, Any
import pandas as pd
import os

data_path = os.path.join(os.path.dirname(__file__), '../../data/mock_medical_data.csv')

class TreatmentAgent:
    def __init__(self):
        self.df = pd.read_csv(data_path)

    def recommend_treatment(self, diagnoses: List[str]) -> List[Dict[str, Any]]:
        treatments = self.df[self.df['disease'].isin(diagnoses)][['disease', 'treatment']].drop_duplicates()
        return treatments.to_dict('records')

if __name__ == "__main__":
    agent = TreatmentAgent()
    print(agent.recommend_treatment(["Flu", "COVID-19"]))
