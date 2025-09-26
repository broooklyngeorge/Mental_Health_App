# inference_engine.py
# This module contains the forward-chaining inference engine.

from knowledge_base import CONDITIONS, INTERVENTIONS

class InferenceEngine:
    def __init__(self):
        self.facts = {} # Working memory to store user responses
        self.fired_rules_log = # For XAI

    def add_fact(self, symptom, value):
        """Adds a fact (user response) to the working memory."""
        self.facts[symptom] = value

    def run(self):
        """Runs the inference engine to determine condition patterns and suggest interventions."""
        detected_conditions =
        
        # Rule Matching and Firing Logic
        # This is a simplified representation of a rule-based system for clarity.
        # A more complex system would use a formal rule representation.
        
        for condition_id, details in CONDITIONS.items():
            present_symptoms = [s for s, v in self.facts.items() if v > 3] # Consider symptoms with severity > 3
            
            # Check core symptoms
            core_symptoms_present = [s for s in details['core_symptoms'] if s in present_symptoms]
            
            # Specificity Check: MDD requires at least one core symptom, GAD requires both, etc.
            core_condition_met = False
            if condition_id == 'MDD' and len(core_symptoms_present) >= 1:
                core_condition_met = True
            elif condition_id == 'GAD' and len(core_symptoms_present) == len(details['core_symptoms']):
                 core_condition_met = True
            elif condition_id in and len(core_symptoms_present) >= 1:
                core_condition_met = True

            if core_condition_met:
                # Check total symptom count against threshold
                other_symptoms_present = [s for s in details.get('other_symptoms',) if s in present_symptoms]
                total_symptoms = len(core_symptoms_present) + len(other_symptoms_present)
                
                if total_symptoms >= details['threshold']:
                    # If rule conditions are met, add to detected conditions
                    detected_conditions.append({
                        'name': details['name'],
                        'explanation': details['explanation'],
                        'symptoms': core_symptoms_present + other_symptoms_present
                    })
                    self.fired_rules_log.append(f"Rule for {details['name']} was triggered.")

        # Suggest interventions based on all reported symptoms
        suggested_interventions = {}
        reported_symptoms = list(self.facts.keys())
        for name, details in INTERVENTIONS.items():
            if any(s in reported_symptoms for s in details['target']):
                suggested_interventions[name] = details['description']

        return detected_conditions, suggested_interventions, self.fired_rules_log