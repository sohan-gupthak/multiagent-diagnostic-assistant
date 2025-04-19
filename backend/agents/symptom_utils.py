from rapidfuzz import process, fuzz
from .symptom_list import SYMPTOM_LIST

def normalize_symptom(symptom):
    return symptom.lower().strip()

import re
import spacy
nlp = spacy.load("en_core_web_sm")

def is_negated(span, doc):
    for tok in span:
        for child in tok.children:
            if child.dep_ == "neg":
                return True
        prev = tok.nbor(-1) if tok.i > 0 else None
        if prev and prev.lower_ in {"no", "not", "without", "denies"}:
            return True
    start = max(0, span.start - 3)
    window = doc[start:span.start].text.lower()
    if any(neg in window for neg in ["no", "not", "without", "denies"]):
        return True
    return False

# Symptom synonym mapping
SYMPTOM_SYNONYMS = {
    "unconscious": "loss of consciousness",
    "unconsciousness": "loss of consciousness",
    "passed out": "loss of consciousness",
    "fainted": "loss of consciousness",
    "blackout": "loss of consciousness",
    "fits": "convulsions",
    "seizure": "convulsions",
    "seizures": "convulsions",
    "tired": "fatigue",
    "tiredness": "fatigue",
    "sweating at night": "night sweats",
    "weight drop": "weight loss",
    "short of breath": "shortness of breath",
    "breathlessness": "shortness of breath",
    "chest tightness": "chest pressure",
    # Add more as needed
}

def extract_medical_symptoms(text):
    doc = nlp(text)
    found = set()
    lowered = text.lower()
    # First, map synonyms in the input to canonical symptoms
    for phrase, canonical in SYMPTOM_SYNONYMS.items():
        if phrase in lowered:
            # Check negation
            idx = lowered.find(phrase)
            neg_window = lowered[max(0, idx-10):idx]
            if not any(neg in neg_window for neg in ["no ", "not ", "without ", "denies "]):
                found.add(canonical)
    # Now, do fuzzy matching as before for canonical symptoms
    for symptom in SYMPTOM_LIST:
        from rapidfuzz import fuzz
        words = lowered.split()
        n = len(symptom.split())
        for i in range(len(words) - n + 1):
            window = " ".join(words[i:i+n])
            score = fuzz.token_set_ratio(window, symptom)
            if score >= 80:
                span = doc.char_span(lowered.find(window), lowered.find(window) + len(window))
                if span is not None:
                    if not is_negated(span, doc):
                        found.add(symptom)
                else:
                    idx = lowered.find(window)
                    if idx != -1:
                        neg_window = lowered[max(0, idx-10):idx]
                        if not any(neg in neg_window for neg in ["no ", "not ", "without ", "denies "]):
                            found.add(symptom)
    return list(found)

def fuzzy_match_symptoms(extracted, known, threshold=80):
    matches = []
    for e in extracted:
        match, score, _ = process.extractOne(e, known, scorer=fuzz.token_sort_ratio)
        if score >= threshold:
            matches.append(match)
    return list(set(matches))

