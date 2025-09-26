# fuzzy_engine.py
# This module implements the fuzzy logic system for assessing symptom severity and calculating a concern level.

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_fuzzy_control_system():
    """
    Creates and configures the fuzzy control system for calculating concern level.
    """
    # Define Antecedents (Inputs) and Consequent (Output)
    # Universe of discourse for inputs and output
    symptom_severity = ctrl.Antecedent(np.arange(0, 11, 1), 'symptom_severity')
    symptom_count = ctrl.Antecedent(np.arange(0, 10, 1), 'symptom_count')
    concern_level = ctrl.Consequent(np.arange(0, 101, 1), 'concern_level')

    # Define Membership Functions using trapezoidal shapes for clear low/medium/high ranges
    symptom_severity['low'] = fuzz.trapmf(symptom_severity.universe, )
    symptom_severity['medium'] = fuzz.trapmf(symptom_severity.universe, )
    symptom_severity['high'] = fuzz.trapmf(symptom_severity.universe, )

    symptom_count['low'] = fuzz.trapmf(symptom_count.universe, )
    symptom_count['medium'] = fuzz.trapmf(symptom_count.universe, )
    symptom_count['high'] = fuzz.trapmf(symptom_count.universe, )
    
    concern_level['low'] = fuzz.trapmf(concern_level.universe, )
    concern_level['moderate'] = fuzz.trapmf(concern_level.universe, )
    concern_level['high'] = fuzz.trapmf(concern_level.universe, )

    # Define Fuzzy Rules
    # These rules encode the expert logic: e.g., high severity and high count -> high concern
    rule1 = ctrl.Rule(symptom_severity['low'] & symptom_count['low'], concern_level['low'])
    rule2 = ctrl.Rule(symptom_severity['medium'] & symptom_count['low'], concern_level['low'])
    rule3 = ctrl.Rule(symptom_severity['low'] & symptom_count['medium'], concern_level['moderate'])
    rule4 = ctrl.Rule(symptom_severity['medium'] & symptom_count['medium'], concern_level['moderate'])
    rule5 = ctrl.Rule(symptom_severity['high'] & symptom_count['medium'], concern_level['high'])
    rule6 = ctrl.Rule(symptom_count['high'], concern_level['high'])
    rule7 = ctrl.Rule(symptom_severity['high'], concern_level['high'])

    # Create the Control System
    concern_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
    
    return concern_ctrl

def calculate_concern_level(fuzzy_system, average_severity, count):
    """
    Calculates a crisp concern level using the fuzzy control system.
    """
    concern_simulation = ctrl.ControlSystemSimulation(fuzzy_system)
    
    # Pass inputs to the ControlSystemSimulation
    concern_simulation.input['symptom_severity'] = average_severity
    concern_simulation.input['symptom_count'] = count
    
    # Compute the result
    concern_simulation.compute()
    
    # Return the defuzzified, crisp output value
    return concern_simulation.output['concern_level']