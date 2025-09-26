# inference_engine.py

from knowledge_base import CONDITIONS, INTERVENTIONS

class InferenceEngine:
    def __init__(self):
        self.facts = {}
        self.fired_rules_log = []

    def add_fact(self, symptom, value):
        self.facts[symptom] = value

    def run(self):
        self.fired_rules_log = []
        detected_conditions = []
        present_symptoms = {s for s, v in self.facts.items() if v >= 5}

        for condition_id, details in CONDITIONS.items():
            core_symptoms_present = [s for s in details['core_symptoms'] if s in present_symptoms]
            
            core_condition_met = False
            if condition_id == 'MDD' and len(core_symptoms_present) >= 1:
                core_condition_met = True
            elif condition_id == 'GAD' and len(core_symptoms_present) == len(details['core_symptoms']):
                core_condition_met = True
            elif condition_id == 'Burnout' and len(core_symptoms_present) >= details.get('threshold', 2):
                core_condition_met = True

            if core_condition_met:
                other_symptoms_present = [s for s in details.get('other_symptoms', []) if s in present_symptoms]
                total_symptoms = len(core_symptoms_present) + len(other_symptoms_present)
                
                if total_symptoms >= details['threshold']:
                    detected_conditions.append({
                        'name': details['name'],
                        'explanation': details['explanation'],
                        'symptoms_matched': core_symptoms_present + other_symptoms_present
                    })
                    self.fired_rules_log.append(
                        f"Rule for '{details['name']}' triggered due to symptoms: {', '.join(core_symptoms_present + other_symptoms_present)}."
                    )

        suggested_interventions = {}
        reported_symptoms = list(self.facts.keys())
        for name, details in INTERVENTIONS.items():
            if any(s in reported_symptoms for s in details['target']):
                suggested_interventions[name] = details['description']

        return detected_conditions, suggested_interventions, self.fired_rules_log
