# knowledge_base.py
# This module contains the expert knowledge for the mental health support system.
# It defines symptoms, conditions, rules, and interventions.

# Symptom definitions with user-facing questions and weights
SYMPTOMS = {
    'depressed_mood': {'question': "Over the last two weeks, have you felt a persistent low or depressed mood for most of the day, nearly every day?", 'weight': 5},
    'loss_of_interest': {'question': "Have you experienced a noticeable loss of interest or pleasure in activities you usually enjoy?", 'weight': 5},
    'weight_change': {'question': "Have you had a significant change in your weight or appetite without trying?", 'weight': 3},
    'sleep_disturbance': {'question': "Have you been sleeping much more or much less than usual nearly every day?", 'weight': 3},
    'psychomotor_change': {'question': "Have others noticed that you are either much more restless or much more slowed down than usual?", 'weight': 4},
    'fatigue': {'question': "Have you been feeling fatigued or a loss of energy nearly every day?", 'weight': 4},
    'worthlessness_guilt': {'question': "Have you had feelings of worthlessness or excessive guilt?", 'weight': 5},
    'concentration_difficulty': {'question': "Have you found it difficult to think, concentrate, or make decisions?", 'weight': 3},
    'suicidal_thoughts': {'question': "Have you had recurrent thoughts of death or suicide?", 'weight': 5},
    
    'excessive_worry': {'question': "For the past six months, have you experienced excessive anxiety and worry about a number of different events or activities?", 'weight': 5},
    'uncontrollable_worry': {'question': "Do you find it very difficult to control your worry?", 'weight': 5},
    'restlessness': {'question': "Have you been feeling restless, keyed up, or on edge?", 'weight': 4},
    'irritability': {'question': "Have you experienced irritability?", 'weight': 3},
    'muscle_tension': {'question': "Have you had muscle tension?", 'weight': 3},

    'work_exhaustion': {'question': "Do you feel a sense of energy depletion or exhaustion primarily related to your work?", 'weight': 5},
    'work_cynicism': {'question': "Have you felt an increased mental distance from your job, or feelings of negativism or cynicism about it?", 'weight': 5},
    'reduced_efficacy': {'question': "Have you noticed a reduction in your professional efficacy or a feeling of being less capable at work?", 'weight': 4},
    
    'identifiable_stressor': {'question': "Have your symptoms developed in response to an identifiable stressful event within the last 3 months?", 'weight': 5},
}

# Condition definitions with required symptoms and thresholds
CONDITIONS = {
    'MDD': {
        'name': "Major Depressive Disorder Pattern",
        'core_symptoms': ['depressed_mood', 'loss_of_interest'], # Must have at least one
        'other_symptoms': ['weight_change', 'sleep_disturbance', 'psychomotor_change', 'fatigue', 'worthlessness_guilt', 'concentration_difficulty', 'suicidal_thoughts'],
        'threshold': 5, # Total symptoms required
        'explanation': "This pattern is characterized by a persistent depressed mood or loss of interest, along with other symptoms like changes in sleep, energy, and feelings of worthlessness."
    },
    'GAD': {
        'name': "Generalized Anxiety Disorder Pattern",
        'core_symptoms': ['excessive_worry', 'uncontrollable_worry'], # Must have both
        'other_symptoms': ['restlessness', 'fatigue', 'concentration_difficulty', 'irritability', 'muscle_tension', 'sleep_disturbance'],
        'threshold': 3, # Additional symptoms required
        'explanation': "This pattern involves excessive and difficult-to-control worry about multiple aspects of life, accompanied by physical symptoms like restlessness and fatigue."
    },
    'Burnout': {
        'name': "Burnout Syndrome Pattern",
        'core_symptoms': ['work_exhaustion', 'work_cynicism', 'reduced_efficacy'], # All three are key dimensions
        'threshold': 2, # At least two should be prominent
        'explanation': "This pattern is specifically related to chronic workplace stress and is defined by feelings of exhaustion, cynicism towards one's job, and a sense of reduced professional accomplishment."
    },
    'Stress': {
        'name': "Stressor-Related Pattern",
        'core_symptoms': ['identifiable_stressor'],
        'threshold': 1,
        'explanation': "This pattern suggests that symptoms have emerged in direct response to a recent, identifiable life stressor."
    }
}

# Evidence-based interventions linked to symptoms
INTERVENTIONS = {
    'Reframing Unhelpful Thoughts': {'target': ['worthlessness_guilt', 'excessive_worry'], 'description': "A core CBT technique to identify, challenge, and change negative thought patterns."},
    'Activity Scheduling': {'target': ['loss_of_interest', 'reduced_efficacy'], 'description': "A Behavioral Activation technique to gradually re-engage in rewarding activities to improve mood and motivation."},
    'Setting Boundaries': {'target': ['work_exhaustion', 'work_cynicism'], 'description': "Strategies to protect your time and energy, especially in a work context, to prevent burnout."},
    'Sleep Hygiene Practices': {'target': ['sleep_disturbance'], 'description': "Practices to improve sleep quality, like sticking to a schedule and creating a relaxing bedtime routine."},
    'Mindfulness & Grounding': {'target': ['restlessness', 'uncontrollable_worry'], 'description': "Techniques like focused breathing to manage acute stress and anxiety by anchoring attention in the present moment."},
    'General Self-Care': {'target': ['fatigue', 'irritability'], 'description': "Focusing on regular exercise, healthy nutrition, and hydration can significantly impact energy levels and mood."}
}
