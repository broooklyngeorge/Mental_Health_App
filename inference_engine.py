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
        
        # A symptom is "present" if its severity is 5 or higher
        present_symptoms = {s for s, v in self.facts.items() if v >= 5}

        # --- STRATEGY 1: CHECK FOR SAFETY-CRITICAL RULES FIRST ---
        safety_rule = CONDITIONS['SAFETY_CRITICAL']
        if 'thoughts_of_harm' in present_symptoms:
            self.fired_rules_log.append("Safety-critical rule triggered. Halting further analysis.")
            return [safety_rule], {'Seek Immediate Help': INTERVENTIONS['Seek Immediate Help']}, self.fired_rules_log

        # --- If no safety issue, proceed with standard analysis ---
        potential_conditions = []
        for condition_id, details in CONDITIONS.items():
            if details.get('priority', 0) >= 100: # Skip the safety rule now
                continue

            core_symptoms_present = [s for s in details['core_symptoms'] if s in present_symptoms]
            
            core_condition_met = False # Basic check to see if rule is a candidate
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
                    # --- Calculate Scores for Justification ---
                    num_defined_symptoms = len(details['core_symptoms']) + len(details.get('other_symptoms', []))
                    
                    # Score 1: Specificity (how detailed is the rule?)
                    specificity_score = num_defined_symptoms
                    
                    # Score 2: Match Strength (how well do the facts fit the rule?)
                    match_score = (total_symptoms_matched / num_defined_symptoms) * 100 if num_defined_symptoms > 0 else 0
                    
                    details['id'] = condition_id
                    details['symptoms_matched'] = core_symptoms_present + other_symptoms_present
                    details['specificity'] = specificity_score
                    details['match'] = match_score
                    potential_conditions.append(details)
                    self.fired_rules_log.append(f"Rule '{details['name']}' considered. Specificity: {specificity_score}, Match: {match_score:.0f}%.")

        # --- STRATEGY 2 & 3: APPLY SPECIFICITY AND MATCH STRENGTH ---
        if not potential_conditions:
            return [], self._get_interventions(present_symptoms, suggestion_history), self.fired_rules_log

        # Sort by priority, then specificity, then match strength. This is the core conflict resolution.
        sorted_conditions = sorted(
            potential_conditions,
            key=lambda x: (x['priority'], x['specificity'], x['match']),
            reverse=True
        )
        
        best_condition = sorted_conditions[0]
        detected_conditions = [best_condition] # Select the single best rule
        self.fired_rules_log.append(f"**Conflict Resolution: '{best_condition['name']}' selected as best fit.**")

        # --- STRATEGY 4: PROVIDE VARIED, NON-REPETITIVE INTERVENTIONS ---
        all_matched_symptoms = set()
        for c in detected_conditions:
            all_matched_symptoms.update(c['symptoms_matched'])

        suggested_interventions = self._get_interventions(all_matched_symptoms, suggestion_history)

        return detected_conditions, suggested_interventions, self.fired_rules_log

    def _get_interventions(self, symptoms, history):
        """Selects relevant and non-repetitive interventions."""
        suggestions = {}
        # Suggest up to 3 interventions
        for _ in range(3):
            best_suggestion = None
            highest_relevance = -1
            
            for name, details in INTERVENTIONS.items():
                # Avoid suggesting what's already been suggested in this session OR what's already in our list
                if name in history or name in suggestions:
                    continue
                
                # Relevance is the number of target symptoms that match the user's symptoms
                relevance = len(set(details['target']) & set(symptoms))
                if relevance > highest_relevance:
                    highest_relevance = relevance
                    best_suggestion = {name: details}
            
            if best_suggestion:
                suggestions.update(best_suggestion)
            else:
                break # No more relevant suggestions to add
        return suggestions
