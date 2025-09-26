# knowledge_base.py

# --- 1. Symptom Definitions ---
# Added new symptoms for Panic, Social Anxiety, and a critical safety check.
SYMPTOMS = {
    # Core Symptoms
    "depressed_mood": "On a scale of 0-10, how would you rate your mood (0 being very low)?",
    "loss_of_interest": "On a scale of 0-10, how would you rate your interest in daily activities?",
    "excessive_worry": "On a scale of 0-10, how much have you been worrying excessively about various things?",
    "fatigue": "On a scale of 0-10, how would you rate your energy level (0 being very fatigued)?",

    # Condition-Specific Symptoms
    "sleep_disturbance": "On a scale of 0-10, how would you rate your sleep quality?",
    "restlessness": "On a scale of 0-10, how restless or on edge have you felt?",
    "cynicism": "On a scale of 0-10, how cynical or detached do you feel from your work/studies?",
    "professional_efficacy": "On a scale of 0-10, how would you rate your sense of professional accomplishment (0 being low)?",
    "panic_attacks": "On a scale of 0-10, have you experienced sudden, intense surges of fear or panic?",
    "fear_of_panic": "On a scale of 0-10, how much do you worry about having another panic attack?",
    "social_fear": "On a scale of 0-10, how intense is your fear of social situations where you might be judged?",
    "social_avoidance": "On a scale of 0-10, how often do you avoid social situations because of this fear?",

    # --- SAFETY CRITICAL SYMPTOM ---
    "thoughts_of_harm": "On a scale of 0-10, have you had any thoughts of harming yourself or others?"
}


# --- 2. Rule Base for Conditions ---
# Added Panic Disorder, Social Anxiety, and a high-priority Safety Rule.
# Each rule now has a 'priority' for the conflict resolution strategy.
CONDITIONS = {
    # --- META-RULE (Highest Priority) ---
    'SAFETY_CRITICAL': {
        'name': 'Immediate Safety Concern',
        'priority': 100,
        'core_symptoms': ['thoughts_of_harm'],
        'threshold': 1, # Requires any score > 5 on the single symptom
        'explanation': 'Your responses indicate thoughts of harm, which requires immediate attention.'
    },

    # --- Clinical Patterns (Standard Priority) ---
    'PanicDisorder': {
        'name': 'Panic Disorder Pattern',
        'priority': 10,
        'core_symptoms': ['panic_attacks', 'fear_of_panic'],
        'other_symptoms': ['restlessness'],
        'threshold': 3, # Both core symptoms must be present, plus restlessness
        'explanation': 'The experience of recurring panic attacks and a persistent fear of having more is a key pattern of Panic Disorder.'
    },
    'SocialAnxiety': {
        'name': 'Social Anxiety Pattern',
        'priority': 10,
        'core_symptoms': ['social_fear', 'social_avoidance'],
        'other_symptoms': ['excessive_worry'],
        'threshold': 3, # Both core symptoms must be present, plus general worry
        'explanation': 'A significant fear of being judged in social situations, leading to avoidance, is characteristic of Social Anxiety.'
    },
    'MDD': {
        'name': 'Major Depressive Disorder Pattern',
        'priority': 10,
        'core_symptoms': ['depressed_mood', 'loss_of_interest'],
        'other_symptoms': ['fatigue', 'sleep_disturbance'],
        'threshold': 3,
        'explanation': 'Your responses show a pattern of low mood and loss of interest, which are key indicators of a depressive episode.'
    },
    'GAD': {
        'name': 'Generalized Anxiety Disorder Pattern',
        'priority': 10,
        'core_symptoms': ['excessive_worry', 'restlessness'],
        'other_symptoms': ['fatigue', 'sleep_disturbance'],
        'threshold': 3,
        'explanation': 'Your responses indicate persistent and excessive worry across various areas of life, which is a hallmark of GAD.'
    },
    'Burnout': {
        'name': 'Burnout Pattern',
        'priority': 5, # Lower priority as it's situational
        'core_symptoms': ['fatigue', 'cynicism', 'professional_efficacy'],
        'other_symptoms': [],
        'threshold': 2,
        'explanation': 'Your responses suggest a combination of exhaustion, cynicism, and a reduced sense of accomplishment, characteristic of burnout.'
    }
}


# --- 3. Expanded Interventions Library ---
# Interventions are now more varied and tagged by modality (CBT, Mindfulness, etc.)
INTERVENTIONS = {
    # --- IMMEDIATE SAFETY INTERVENTION ---
    'Seek Immediate Help': {
        'modality': 'Crisis Support',
        'target': ['thoughts_of_harm'],
        'description': 'Please contact a crisis hotline, a mental health professional, or emergency services immediately. Your safety is the top priority.'
    },

    # --- Grounding & Mindfulness Techniques ---
    '5-4-3-2-1 Grounding': {
        'modality': 'Mindfulness',
        'target': ['panic_attacks', 'restlessness', 'excessive_worry'],
        'description': 'Ground yourself in the present moment. Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.'
    },
    'Mindful Breathing': {
        'modality': 'Mindfulness',
        'target': ['panic_attacks', 'excessive_worry', 'restlessness'],
        'description': 'Focus on your breath. Inhale slowly for 4 counts, hold for 4, and exhale slowly for 6. Repeat for 2-3 minutes to calm your nervous system.'
    },
    'Body Scan Meditation': {
        'modality': 'Mindfulness',
        'target': ['sleep_disturbance', 'fatigue'],
        'description': 'Lie down and bring gentle, non-judgmental attention to each part of your body, from your toes to your head. This can reduce tension.'
    },

    # --- Cognitive Behavioral Therapy (CBT) Techniques ---
    'Cognitive Reframing': {
        'modality': 'CBT',
        'target': ['excessive_worry', 'cynicism', 'social_fear'],
        'description': "Challenge a negative thought. Ask yourself: What's the evidence for this thought? Is there a more balanced way of looking at this?"
    },
    'Worry Postponement': {
        'modality': 'CBT',
        'target': ['excessive_worry'],
        'description': 'Set aside a specific 15-minute "worry time" each day. When a worry comes up outside this time, jot it down and defer it until your worry time.'
    },
    'Graded Exposure': {
        'modality': 'CBT',
        'target': ['social_avoidance', 'fear_of_panic'],
        'description': 'Create a list of feared situations, from least scary to most. Gradually and repeatedly practice facing these situations to build confidence.'
    },

    # --- Behavioral Techniques ---
    'Behavioral Activation': {
        'modality': 'Behavioral',
        'target': ['depressed_mood', 'loss_of_interest'],
        'description': 'Schedule one small, positive activity for tomorrow, even if you don\'t feel like it (e.g., a 10-minute walk, listening to one song).'
    },
    'Sleep Hygiene Improvement': {
        'modality': 'Behavioral',
        'target': ['sleep_disturbance', 'fatigue'],
        'description': 'Strengthen your sleep routine. Aim for a consistent wake-up time, avoid screens an hour before bed, and ensure your room is dark and cool.'
    },
    'Setting Boundaries': {
        'modality': 'Behavioral',
        'target': ['cynicism', 'professional_efficacy'],
        'description': 'Identify one clear boundary to set at work or school (e.g., "I will not check emails after 7 PM") to protect your energy and time.'
    }
}
