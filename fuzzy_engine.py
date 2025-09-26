# fuzzy_engine.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_fuzzy_control_system():
    mood = ctrl.Antecedent(np.arange(0, 11, 1), 'mood')
    interest = ctrl.Antecedent(np.arange(0, 11, 1), 'interest')
    worry = ctrl.Antecedent(np.arange(0, 11, 1), 'worry')
    concern = ctrl.Consequent(np.arange(0, 11, 1), 'concern')

    mood['low'] = fuzz.trapmf(mood.universe, [0, 0, 2, 4])
    mood['medium'] = fuzz.trapmf(mood.universe, [3, 4, 6, 7])
    mood['high'] = fuzz.trapmf(mood.universe, [6, 8, 10, 10])

    interest['low'] = fuzz.trapmf(interest.universe, [0, 0, 2, 4])
    interest['medium'] = fuzz.trapmf(interest.universe, [3, 4, 6, 7])
    interest['high'] = fuzz.trapmf(interest.universe, [6, 8, 10, 10])

    worry['low'] = fuzz.trapmf(worry.universe, [0, 0, 2, 4])
    worry['medium'] = fuzz.trapmf(worry.universe, [3, 4, 6, 7])
    worry['high'] = fuzz.trapmf(worry.universe, [6, 8, 10, 10])

    concern['low'] = fuzz.trapmf(concern.universe, [0, 0, 2, 4])
    concern['moderate'] = fuzz.trapmf(concern.universe, [3, 4, 6, 7])
    concern['high'] = fuzz.trapmf(concern.universe, [6, 8, 10, 10])

    rule1 = ctrl.Rule(mood['low'] & interest['low'], concern['high'])
    rule2 = ctrl.Rule(worry['high'], concern['high'])
    rule3 = ctrl.Rule(mood['medium'] | interest['medium'] | worry['medium'], concern['moderate'])
    rule4 = ctrl.Rule(mood['high'] & interest['high'] & worry['low'], concern['low'])

    concern_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
    return ctrl.ControlSystemSimulation(concern_ctrl)

def calculate_concern_level(simulation, user_inputs):
    try:
        simulation.input['mood'] = user_inputs.get('depressed_mood', 5)
        simulation.input['interest'] = user_inputs.get('loss_of_interest', 5)
        simulation.input['worry'] = user_inputs.get('excessive_worry', 5)
        simulation.compute()
        return simulation.output['concern']
    except Exception as e:
        print(f"Fuzzy calculation error: {e}")
        return 5.0
