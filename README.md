# Multi-Agent AI-Powered Diagnostic Assistant

This project is an end-to-end, multi-agent diagnostic assistant for healthcare professionals. It uses open-source tools and the Google Agent Development Kit (ADK) to analyze patient symptoms and history, suggest diagnoses, recommend treatments, and provide preliminary health assessments.

## Features
- **NLP Agent:** Parses and interprets symptom descriptions and medical history.
- **Diagnosis Agent:** Suggests possible diagnoses using open/mock data.
- **Treatment Agent:** Recommends treatments for suggested diagnoses.
- **Symptom Checker Agent:** Provides urgent/non-urgent assessment.
- **Coordinator:** Orchestrates the workflow using ADK.
- **Doctor-friendly Web UI:** (To be implemented in `frontend/`)

## Backend Setup
1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
2. Run the API server:
   ```bash
   python app.py
   ```

## API Usage
POST `/api/diagnose` with JSON body:
```json
{
  "user_input": "Patient reports fever, cough, and shortness of breath for 3 days."
}
```

Returns:
- Parsed symptoms
- Top diagnoses
- Recommended treatments
- Urgency assessment

## Data
- Uses `data/mock_medical_data.csv` for demo purposes. Replace with real/open medical datasets for production use.

## Privacy & Ethics
- No patient data is stored. All processing is in-memory for demo.
- For real deployments, ensure compliance with medical data privacy laws (e.g., HIPAA, GDPR).

## (Bonus) Voice & Wearable Integration
- Voice input and wearable data integration can be added in the frontend using browser APIs and mock data.

---

## Next Steps
- Implement the React frontend in `frontend/`.
- Expand mock data or connect to real medical datasets.
- Add authentication and audit logging for clinical use.

# System Architecture & Flow

This section explains how the multi-agent AI Diagnostic Assistant processes a user prompt, orchestrates agent reasoning, and produces clinically robust output. Use this for technical understanding or presentations.

## 1. User Prompt/Input
- **Frontend:** User enters a clinical scenario or patient history (e.g., symptoms, context) into the web interface.
- **Example:**
  > Patient was found unconscious and had convulsions for about one minute. On regaining consciousness, the patient was confused and had a headache. No fever or chest pain.

## 2. API Request
- The frontend sends this input as a POST request to the backend API endpoint (`/api/diagnose`).

## 3. Coordinator Orchestration
- The backend `Coordinator` class receives the input and orchestrates a pipeline of specialized agents.
- **Coordinator’s Role:**
  - Aggregates the outputs of all agents.
  - Ensures the response is comprehensive and clinically robust.

## 4. Agent Pipeline (Modular Multi-Agent System)

### a. NLP Agent (Symptom Extraction)
- **Purpose:** Extracts and normalizes symptoms from the raw text.
- **How:**
  - Uses spaCy for NLP parsing.
  - Applies fuzzy matching and synonym mapping (e.g., “fainted” → “loss of consciousness”).
  - Detects and ignores negated symptoms (e.g., “No fever”).
- **Output:**
  - `["convulsions", "confusion", "headache", "loss of consciousness"]`

### b. Comorbidity Agent
- **Purpose:** Identifies chronic illnesses and risk factors from the input.
- **How:** Searches for keywords (e.g., “diabetes”, “smoking”).
- **Output:** `["smoking", "diabetes"]` (if present)

### c. Diagnosis Agent
- **Purpose:** Suggests likely diagnoses based on extracted symptoms.
- **How:**
  - Matches symptoms against a database (CSV) of known symptom-disease pairs.
  - **Red flag logic:** If critical symptoms are present (e.g., “convulsions”), prioritizes emergency diagnoses (e.g., “Seizure”).
- **Output:** `["Seizure", "Epilepsy", "Post-ictal state"]`

### d. Differential Diagnosis Agent
- **Purpose:** Suggests alternative/related diagnoses.
- **How:** Maps symptoms to a curated set of possible differentials.
- **Output:** `["Meningitis", "Encephalitis"]` (if mapped)

### e. Red Flag Agent
- **Purpose:** Detects symptoms that require urgent action.
- **How:** Checks for presence of critical symptoms (e.g., “loss of consciousness”, “chest pain”).
- **Output:** `["loss of consciousness", "convulsions"]`

### f. Guideline Agent
- **Purpose:** Checks suggested diagnoses against evidence-based guidelines.
- **How:** Provides standard-of-care recommendations for each diagnosis.
- **Output:** `"Seizure: Immediate evaluation, imaging, labs"`

### g. Treatment Agent
- **Purpose:** Suggests treatments for each diagnosis.
- **How:** Looks up treatments in a database or mapping.
- **Output:** `{ "Seizure": "Urgent medical evaluation" }`

### h. (Optional) Gemini Agent
- **Purpose:** Uses Google Gemini API for advanced reasoning or as a fallback for complex cases.
- **How:** Sends the input and/or intermediate results to Gemini for further analysis or validation.
- **Output:** May refine or supplement the above outputs.

## 5. Aggregation and Response Construction
- The `Coordinator` collects all agent outputs and builds a structured response:
  - **Parsed Symptoms**
  - **Comorbidities**
  - **Top Diagnoses**
  - **Differential Diagnoses**
  - **Red Flags**
  - **Treatments**
  - **Guidelines**
  - **Assessment** (e.g., “Seek urgent/emergency care!”)

## 6. Frontend Display
- The frontend displays the results in a user-friendly format, highlighting urgent findings and actionable recommendations.

## Visual Flow Diagram

```
User Input (Frontend)
        |
        v
API Request (/api/diagnose)
        |
        v
Coordinator (Backend)
        |
        +----------------------------+
        |                            |
   [NLP Agent]                 [Comorbidity Agent]
        |                            |
   [Diagnosis Agent]           [Red Flag Agent]
        |                            |
   [Differential Dx Agent]     [Guideline Agent]
        |                            |
   [Treatment Agent]           [Gemini Agent (optional)]
        |                            |
        +----------------------------+
                  |
                  v
        Aggregated Response
                  |
                  v
           Frontend Display
```

### Key Points
- **Multi-Agent Orchestration:** Each agent specializes in a clinical reasoning task, and their outputs are combined for accuracy and safety.
- **NLP Robustness:** Modern NLP (spaCy + fuzzy matching + synonym mapping) ensures reliable symptom extraction.
- **Red Flag Safety:** Emergency symptoms are always prioritized and flagged.
- **Extensibility:** New agents (e.g., Gemini-powered) can be added for advanced reasoning or validation.
- **Clinical-Grade Output:** The system is designed to minimize missed emergencies and provide actionable, guideline-based recommendations.

