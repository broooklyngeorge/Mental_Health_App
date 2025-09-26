# inference_engine.py

from knowledge_base import CONDITIONS, INTERVENTIONS

class InferenceEngine:
    def __init__(self):
        self.facts = {}
        self.fired_rules_log = []

    def add_fact(self, symptom, value):
        self.facts[symptom] = value

    def run(self, suggestion_history=None):
        if suggestion_history is None:
            suggestion_history = []
            
        self.fired_rules_log = []
        
        present_symptoms = {s for s, v in self.facts.items() if v >= 5}

        # --- STRATEGY 1: CHECK FOR SAFETY-CRITICAL RULES FIRST ---
        if 'thoughts_of_harm' in present_symptoms:
            self.fired_rules_log.append("Safety-critical rule triggered. Halting further analysis.")
            safety_rule = CONDITIONS['SAFETY_CRITICAL'].copy() # Use .copy() to avoid modifying the original
            safety_rule['id'] = 'SAFETY_CRITICAL' # ** THIS LINE FIXES THE KeyError **
            return [safety_rule], {'Seek Immediate Help': INTERVENTIONS['Seek Immediate Help']}, self.fired_rules_log

        # --- If no safety issue, proceed with standard analysis ---
        potential_conditions = []
        for condition_id, details in CONDITIONS.items():
            if details.get('priority', 0) >= 100:
                continue

            core_symptoms_present = [s for s in details['core_symptoms'] if s in present_symptoms]
            
            core_condition_met = False
            if condition_id in ['MDD', 'GAD'] and len(core_symptoms_present) >= 1:
                core_condition_met = True
            elif condition_id in ['PanicDisorder', 'SocialAnxiety'] and len(core_symptoms_present) == len(details['core_symptoms']):
                core_condition_met = True
            elif condition_id == 'Burnout' and len(core_symptoms_present) >= 1:
                 core_condition_met = True

            if core_condition_met:
                other_symptoms_present = [s for s in details.get('other_symptoms', []) if s in present_symptoms]
                total_symptoms_matched = len(core_symptoms_present) + len(other_symptoms_present)
                
                if total_symptoms_matched >= details['threshold']:
                    num_defined_symptoms = len(details['core_symptoms']) + len(details.get('other_symptoms', []))
                    
                    specificity_score = num_defined_symptoms
                    match_score = (total_symptoms_matched / num_defined_symptoms) * 100 if num_defined_symptoms > 0 else 0
                    
                    # Create a copy to avoid modifying the original KNOWLEDGE_BASE constant
                    condition_data = details.copy()
                    condition_data['id'] = condition_id
                    condition_data['symptoms_matched'] = core_symptoms_present + other_symptoms_present
                    condition_data['specificity'] = specificity_score
                    condition_data['match'] = match_score
                    
                    potential_conditions.append(condition_data)
                    self.fired_rules_log.append(f"Rule '{details['name']}' considered. Specificity: {specificity_score}, Match: {match_score:.0f}%.")

        if not potential_conditions:
            return [], self._get_interventions(present_symptoms, suggestion_history), self.fired_rules_log

        sorted_conditions = sorted(
            potential_conditions,
            key=lambda x: (x['priority'], x['specificity'], x['match']),
            reverse=True
        )
        
        best_condition = sorted_conditions[0]
        detected_conditions = [best_condition]
        self.fired_rules_log.append(f"**Conflict Resolution: '{best_condition['name']}' selected as best fit.**")

        all_matched_symptoms = set()
        for c in detected_conditions:
            all_matched_symptoms.update(c['symptoms_matched'])

        suggested_interventions = self._get_interventions(all_matched_symptoms, suggestion_history)

        return detected_conditions, suggested_interventions, self.fired_rules_log

    def _get_interventions(self, symptoms, history):
        suggestions = {}
        for _ in range(3):
            best_suggestion = None
            highest_relevance = -1
            
            for name, details in INTERVENTIONS.items():
                if name in history or name in suggestions or name == "Seek Immediate Help":
                    continue
                
                relevance = len(set(details['target']) & set(symptoms))
                if relevance > highest_relevance:
                    highest_relevance = relevance
                    best_suggestion = {name: details}
            
            if best_suggestion:
                suggestions.update(best_suggestion)
            else:
                break
        return suggestions
