import requests
from typing import Dict, Any
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gemini_config import GEMINI_API_KEY

class GeminiAgent:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    def analyze(self, user_input: str) -> Dict[str, Any]:
        prompt = f"""
You are a highly reliable medical AI assistant. Analyze the following patient input and perform the following:
1. Extract all possible medical symptoms mentioned (at least 2-3 if present).
2. Suggest at least 2-3 possible diagnoses, based on the symptoms and context.
3. Recommend at least 2-3 treatments or next steps for each diagnosis.
4. Assess urgency (e.g., emergency, urgent, routine) and explain why.

Format your response as a JSON object with these fields:
- symptoms: list of strings
- diagnoses: list of strings
- treatments: list of strings (treatment or next step, optionally prefixed by diagnosis)
- urgency: string (with a short explanation)

Be as comprehensive and medically accurate as possible. If information is missing, make reasonable clinical assumptions. Do not omit any important findings.

Patient input: {user_input}
"""
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        try:
            resp = requests.post(self.endpoint, headers=headers, params=params, json=data, timeout=20)
            resp.raise_for_status()
            text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            import json
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != -1:
                return json.loads(text[start:end])
            else:
                return {"error": "Could not parse Gemini response"}
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    agent = GeminiAgent()
    print(agent.analyze("Patient reports fever, cough, and shortness of breath for 3 days."))
