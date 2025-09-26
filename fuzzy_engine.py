# fuzzy_engine.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_fuzzy_control_system():
    """Creates and returns the fuzzy control system and its simulation."""
    # Define Antecedents (Inputs) on a 0-10 scale
    mood = ctrl.Antecedent(np.arange(0, 11, 1), 'mood')
    interest = ctrl.Antecedent(np.arange(0, 11, 1), 'interest')
    worry = ctrl.Antecedent(np.arange(0, 11, 1), 'worry')

    # Define Consequent (Output) on a 0-10 scale
    concern = ctrl.Consequent(np.arange(0, 11, 1), 'concern')

    # Define Membership Functions for Inputs using trapezoidal shapes
    # Format: [start, peak_start, peak_end, end]
    mood['low'] = fuzz.trapmf(mood.universe, [0, 0, 2, 4])
    mood['medium'] = fuzz.trapmf(mood.universe, [3, 4, 6, 7])
    mood['high'] = fuzz.trapmf(mood.universe, [6, 8, 10, 10])

    interest['low'] = fuzz.trapmf(interest.universe, [0, 0, 2, 4])
    interest['medium'] = fuzz.trapmf(interest.universe, [3, 4, 6, 7])
    interest['high'] = fuzz.trapmf(interest.universe, [6, 8, 10, 10])

    worry['low'] = fuzz.trapmf(worry.universe, [0, 0, 2, 4])
    worry['medium'] = fuzz.trapmf(worry.universe, [3, 4, 6, 7])
    worry['high'] = fuzz.trapmf(worry.universe, [6, 8, 10, 10])

    # Define Membership Functions for Output
    concern['low'] = fuzz.trapmf(concern.universe, [0, 0, 2, 4])
    concern['moderate'] = fuzz.trapmf(concern.universe, [3, 4, 6, 7])
    concern['high'] = fuzz.trapmf(concern.universe, [6, 8, 10, 10])

    # Define Fuzzy Rules
    rule1 = ctrl.Rule(mood['low'] & interest['low'], concern['high'])
    rule2 = ctrl.Rule(worry['high'], concern['high'])
    rule3 = ctrl.Rule(mood['medium'] | interest['medium'] | worry['medium'], concern['moderate'])
    rule4 = ctrl.Rule(mood['high'] & interest['high'] & worry['low'], concern['low'])

    # Create Control System
    concern_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
    concern_simulation = ctrl.ControlSystemSimulation(concern_ctrl)
    
    return concern_simulation

def calculate_concern_level(simulation, user_inputs):
    """Calculates and returns the defuzzified concern level."""
    try:
        # Provide default neutral values if a symptom isn't in the user_inputs dict
        simulation.input['mood'] = user_inputs.get('depressed_mood', 5)
        simulation.input['interest'] = user_inputs.get('loss_of_interest', 5)
        simulation.input['worry'] = user_inputs.get('excessive_worry', 5)
        
        # Compute the result
        simulation.compute()
        
        return simulation.output['concern']
    except Exception as e:
        # Fallback to a neutral value if any error occurs during fuzzy computation
        print(f"Fuzzy calculation error: {e}")
        return 5.0
