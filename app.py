# app.py

import streamlit as st
import numpy as np  # Added this import to fix the NameError
from knowledge_base import SYMPTOMS
from inference_engine import InferenceEngine
from fuzzy_engine import create_fuzzy_control_system, calculate_concern_level

def initialize_session_state():
    """Initializes variables in Streamlit's session state."""
    if 'symptom_inputs' not in st.session_state:
        # Default all symptoms to a neutral value of 5
        st.session_state.symptom_inputs = {symptom_id: 5 for symptom_id in SYMPTOMS.keys()}
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'fuzzy_system' not in st.session_state:
        # Create and store the fuzzy system once per session
        st.session_state.fuzzy_system = create_fuzzy_control_system()

# --- Page Configuration ---
st.set_page_config(
    page_title="Mindful AI Advisor",
    page_icon="🧠",
    layout="wide"
)

# --- Initialize ---
initialize_session_state()
engine = InferenceEngine()

# --- UI Layout ---
st.title("🧠 Mindful AI Advisor")
st.markdown(
    "This is an educational tool demonstrating an expert system. "
    "It is **not** a substitute for professional medical advice."
)

# --- Sidebar for User Input ---
with st.sidebar:
    st.header("Symptom Assessment")
    st.markdown("Rate your feelings over the last two weeks from 0 (Not at all) to 10 (Constantly).")
    
    # Create a slider for each symptom
    for symptom_id, question in SYMPTOMS.items():
        st.session_state.symptom_inputs[symptom_id] = st.slider(
            question, 0, 10, st.session_state.symptom_inputs[symptom_id]
        )

    # Analyze button
    analyze_button = st.button("Analyze My Responses", type="primary")

    # Reset button
    if st.button("Reset"):
        st.session_state.symptom_inputs = {symptom_id: 5 for symptom_id in SYMPTOMS.keys()}
        st.session_state.results = None
        st.rerun()


# --- Main Panel for Results ---
if analyze_button:
    # Add all user inputs as facts to the inference engine
    for symptom_id, value in st.session_state.symptom_inputs.items():
        engine.add_fact(symptom_id, value)
    
    # Run the rule-based engine
    conditions, interventions, log = engine.run()
    
    # Run the fuzzy logic engine - CORRECTED CALL
    concern_level = calculate_concern_level(
        st.session_state.fuzzy_system,
        st.session_state.symptom_inputs  # Pass the entire dictionary of inputs
    )
    
    # Store results in session state
    st.session_state.results = {
        "conditions": conditions,
        "interventions": interventions,
        "log": log,
        "concern": concern_level
    }

# --- Display Results ---
if st.session_state.results:
    results = st.session_state.results
    st.markdown("---")
    st.header("Assessment Results")

    # Display Fuzzy Logic Concern Level
    st.subheader("Fuzzy Logic Concern Level")
    st.progress(results['concern'] / 10.0)
    st.info(
        f"Based on your mood, interest, and worry levels, the system calculated a general concern score of "
        f"**{results['concern']:.2f} out of 10**. This provides a blended, nuanced view of your inputs."
    )

    # Display Detected Patterns (from Inference Engine)
    st.subheader("Detected Symptom Patterns")
    if not results['conditions']:
        st.success("No specific symptom patterns were strongly detected based on the defined rules.")
    else:
        for condition in results['conditions']:
            with st.container(border=True):
                st.markdown(f"#### {condition['name']}")
                st.write(condition['explanation'])
                st.caption(f"**Matched Symptoms:** {', '.join(condition['symptoms_matched'])}")

    # Display Suggested Interventions
    st.subheader("Suggested Self-Help Interventions")
    if not results['interventions']:
        st.write("No specific interventions to suggest at this time.")
    else:
        for name, desc in results['interventions'].items():
            st.markdown(f"**{name}:** {desc}")
    
    # Display Explainable AI (XAI) Log
    with st.expander("Show Explanation Log (XAI)"):
        st.write("This log shows which rules in the expert system were triggered during the analysis.")
        if not results['log']:
            st.write("No rules were triggered.")
        else:
            for entry in results['log']:
                st.code(entry, language='text')

else:
    st.info("Please adjust the sliders in the sidebar and click 'Analyze My Responses' to see your results.")
