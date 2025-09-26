# knowledge_base.py

SYMPTOMS = {
    "depressed_mood": "On a scale of 0 to 10, how would you rate your mood (0 being very low)?",
    "loss_of_interest": "On a scale of 0 to 10, how would you rate your interest in daily activities?",
    "fatigue": "On a scale of 0 to 10, how would you rate your energy level (0 being very fatigued)?",
    "sleep_disturbance": "On a scale of 0 to 10, how would you rate your sleep quality?",
    "excessive_worry": "On a scale of 0 to 10, how much have you been worrying excessively?",
    "restlessness": "On a scale of 0 to 10, how restless or on edge have you felt?",
    "cynicism": "On a scale of 0 to 10, how cynical or detached do you feel from your work?",
    "professional_efficacy": "On a scale of 0 to 10, how would you rate your sense of professional accomplishment (0 being very low)?"
}

CONDITIONS = {
    'MDD': {
        'name': 'Major Depressive Disorder Pattern',
        'core_symptoms': ['depressed_mood', 'loss_of_interest'],
        'other_symptoms': ['fatigue', 'sleep_disturbance'],
        'threshold': 3,
        'explanation': 'Your responses show a pattern of low mood and loss of interest, which are key indicators of a depressive episode.'
    },
    'GAD': {
        'name': 'Generalized Anxiety Disorder Pattern',
        'core_symptoms': ['excessive_worry', 'restlessness'],
        'other_symptoms': ['fatigue'],
        'threshold': 3,
        'explanation': 'Your responses indicate persistent and excessive worry and restlessness, which are hallmarks of an anxiety pattern.'
    },
    'Burnout': {
        'name': 'Burnout Pattern',
        'core_symptoms': ['fatigue', 'cynicism', 'professional_efficacy'],
        'other_symptoms': [],
        'threshold': 2,
        'explanation': 'Your responses suggest a combination of exhaustion, cynicism, and a reduced sense of accomplishment, which are characteristic of burnout.'
    }
}

INTERVENTIONS = {
    'Mindful Breathing': {
        'target': ['excessive_worry', 'restlessness'],
        'description': 'Practice slow, deep breathing for 5-10 minutes. This can help calm your nervous system.'
    },
    'Behavioral Activation': {
        'target': ['depressed_mood', 'loss_of_interest'],
        'description': 'Schedule one small, enjoyable activity for tomorrow. Re-engaging with positive activities can help lift your mood.'
    },
    'The 5-4-3-2-1 Method': {
        'target': ['restlessness', 'excessive_worry'],
        'description': 'Ground yourself by naming: 5 things you see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste.'
    },
    'Setting Boundaries': {
        'target': ['cynicism', 'professional_efficacy'],
        'description': 'Identify one area at work to set a clear boundary, such as not checking emails after a certain hour, to protect your personal time.'
    },
    'Sleep Hygiene': {
        'target': ['sleep_disturbance', 'fatigue'],
        'description': 'Improve sleep by creating a routine: go to bed and wake up at the same time, and avoid screens an hour before bed.'
    }
}
