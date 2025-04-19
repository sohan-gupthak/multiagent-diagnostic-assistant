# Coordinator Agent: Orchestrates the workflow using Google ADK
from agents.nlp_agent import NLPAgent
from agents.diagnosis_agent import DiagnosisAgent
from agents.treatment_agent import TreatmentAgent
from agents.symptom_checker_agent import SymptomCheckerAgent
from agents.gemini_agent import GeminiAgent
from agents.differential_diagnosis_agent import DifferentialDiagnosisAgent
from agents.red_flag_agent import RedFlagAgent
from agents.comorbidity_agent import ComorbidityAgent
from agents.guideline_agent import GuidelineAgent

class Coordinator:
    def __init__(self, use_gemini: bool = True):
        self.nlp_agent = NLPAgent()
        self.diagnosis_agent = DiagnosisAgent()
        self.treatment_agent = TreatmentAgent()
        self.symptom_checker_agent = SymptomCheckerAgent()
        self.differential_agent = DifferentialDiagnosisAgent()
        self.red_flag_agent = RedFlagAgent()
        self.comorbidity_agent = ComorbidityAgent()
        self.guideline_agent = GuidelineAgent()
        self.use_gemini = use_gemini
        if self.use_gemini:
            self.gemini_agent = GeminiAgent()

    def process(self, user_input: str):
        gemini_result = None
        if self.use_gemini:
            gemini_result = self.gemini_agent.analyze(user_input)
            gemini_symptoms = gemini_result.get("symptoms") if gemini_result and not gemini_result.get("error") else []
            gemini_diagnoses = gemini_result.get("diagnoses") if gemini_result and not gemini_result.get("error") else []
            gemini_treatments = gemini_result.get("treatments") if gemini_result and not gemini_result.get("error") else []
            gemini_urgency = gemini_result.get("urgency") if gemini_result and not gemini_result.get("error") else ""
        else:
            gemini_symptoms, gemini_diagnoses, gemini_treatments, gemini_urgency = [], [], [], ""

        # Always run local pipeline
        nlp_result = self.nlp_agent.parse_input(user_input)
        local_symptoms = nlp_result["symptoms"]
        local_diagnoses = self.diagnosis_agent.diagnose(local_symptoms)
        local_diagnosis_names = [d["disease"] for d in local_diagnoses]
        local_treatments = self.treatment_agent.recommend_treatment(local_diagnosis_names)
        local_assessment = self.symptom_checker_agent.check(local_symptoms)

        # Merge results: prefer local data if Gemini is incomplete
        symptoms = gemini_symptoms if gemini_symptoms and len(gemini_symptoms) >= len(local_symptoms) else local_symptoms
        diagnoses = (
            [{"disease": d, "count": 1} for d in gemini_diagnoses]
            if gemini_diagnoses and len(gemini_diagnoses) >= len(local_diagnosis_names)
            else local_diagnoses
        )
        treatments = (
            [{"disease": t.split(":")[0], "treatment": t.split(":",1)[-1].strip()} for t in gemini_treatments]
            if gemini_treatments and len(gemini_treatments) >= len(local_treatments)
            else local_treatments
        )
        assessment = {"urgent": "urgent" in (gemini_urgency or '').lower(), "message": gemini_urgency or local_assessment.get("message", "")}

        # Improvement agents for flaws
        differentials = self.differential_agent.suggest_differentials(symptoms)
        red_flags = self.red_flag_agent.check_red_flags(user_input, symptoms)
        comorbidities = self.comorbidity_agent.extract_comorbidities(user_input)
        guideline_recs = self.guideline_agent.check_guidelines([d['disease'] for d in diagnoses])

        return {
            "parsed_symptoms": symptoms,
            "diagnoses": diagnoses,
            "treatments": treatments,
            "assessment": assessment,
            "differential_diagnoses": differentials,
            "red_flags": red_flags,
            "comorbidities": comorbidities,
            "guidelines": guideline_recs,
            "gemini": self.use_gemini,
            "debug": {
                "gemini_raw": gemini_result,
                "local_symptoms": local_symptoms,
                "local_diagnoses": local_diagnoses,
                "local_treatments": local_treatments,
                "local_assessment": local_assessment
            }
        }

if __name__ == "__main__":
    coordinator = Coordinator(use_gemini=True)
    result = coordinator.process("Patient reports fever, cough, and shortness of breath for 3 days.")
    print(result)
