# app.py

import streamlit as st
import numpy as np
from knowledge_base import SYMPTOMS, INTERVENTIONS
from inference_engine import InferenceEngine
from fuzzy_engine import create_fuzzy_control_system, calculate_concern_level

def initialize_session_state():
    """Initializes all necessary variables in Streamlit's session state."""
    if 'symptom_inputs' not in st.session_state:
        st.session_state.symptom_inputs = {symptom_id: 0 for symptom_id in SYMPTOMS.keys()}
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'fuzzy_system' not in st.session_state:
        st.session_state.fuzzy_system = create_fuzzy_control_system()
    if 'suggestion_history' not in st.session_state:
        st.session_state.suggestion_history = []

def main():
    """The main function that runs the Streamlit application."""
    st.set_page_config(page_title="Mindful AI Advisor", page_icon="🧠", layout="wide")
    initialize_session_state()
    engine = InferenceEngine()

    st.title("🧠 Mindful AI Advisor")
    st.markdown("This is an educational tool. It is **not** a substitute for professional medical advice.")

    with st.sidebar:
        st.header("Symptom Assessment")
        st.markdown("Over the last two weeks, rate each from 0 (Not at all) to 10 (Constantly).")
        
        # Create sliders for all symptoms, with the safety question last
        symptom_keys = list(SYMPTOMS.keys())
        safety_key = "thoughts_of_harm"
        symptom_keys.remove(safety_key)
        
        for symptom_id in symptom_keys:
            st.session_state.symptom_inputs[symptom_id] = st.slider(
                SYMPTOMS[symptom_id], 0, 10, st.session_state.symptom_inputs[symptom_id], key=symptom_id
            )
        
        st.markdown("---")
        st.session_state.symptom_inputs[safety_key] = st.slider(
            f"**{SYMPTOMS[safety_key]}**", 0, 10, st.session_state.symptom_inputs[safety_key], key=safety_key
        )

        analyze_button = st.button("Analyze My Responses", type="primary")
        if st.button("Reset"):
            st.session_state.clear()
            st.rerun()

    if analyze_button:
        for symptom_id, value in st.session_state.symptom_inputs.items():
            engine.add_fact(symptom_id, value)
        
        conditions, interventions, log = engine.run(st.session_state.suggestion_history)
        concern_level = calculate_concern_level(st.session_state.fuzzy_system, st.session_state.symptom_inputs)
        
        st.session_state.results = {
            "conditions": conditions,
            "interventions": interventions,
            "log": log,
            "concern": concern_level
        }
        # Update history to prevent future repetition in this session
        st.session_state.suggestion_history.extend(interventions.keys())

    if st.session_state.results:
        results = st.session_state.results
        
        # --- STRATEGY 5: HANDLE ETHICAL META-RULES IN THE UI ---
        # If the safety rule was triggered, display a special message and nothing else.
        if results['conditions'] and results['conditions'][0]['id'] == 'SAFETY_CRITICAL':
            st.error("### Immediate Safety Concern", icon="⚠️")
            st.markdown(
                "Your responses have indicated a potential safety risk. The analysis has been stopped. "
                "Your well-being is the most important thing, and we strongly urge you to seek immediate support."
            )
            st.subheader("Recommended Action:")
            st.warning(INTERVENTIONS['Seek Immediate Help']['description'])
            st.markdown("---")
            st.markdown(
                "Other resources: "
                "\n- **Emergency Services:** Call 911 or your local emergency number."
                "\n- **Crisis Text Line:** Text HOME to 741741."
                "\n- **The National Suicide Prevention Lifeline:** Call or text 988."
            )
        else:
            # --- Standard Results Display ---
            st.markdown("---")
            st.header("Assessment Results")
            st.subheader("Fuzzy Logic Concern Level")
            st.progress(results['concern'] / 10.0)
            st.info(f"The system calculated a general concern score of **{results['concern']:.2f} out of 10**.")

            st.subheader("Primary Symptom Pattern Detected")
            if not results['conditions']:
                st.success("No single, strong symptom pattern was detected based on your responses.")
            else:
                for condition in results['conditions']:
                    with st.container(border=True):
                        st.markdown(f"#### {condition['name']}")
                        st.write(condition['explanation'])
                        st.caption(f"**Justification:** This pattern was selected due to the highest rule specificity and match strength.")

            st.subheader("Personalized Intervention Suggestions")
            if not results['interventions']:
                st.write("No specific interventions to suggest at this time.")
            else:
                for name, details in results['interventions'].items():
                    st.markdown(f"**{name} ({details['modality']}):** {details['description']}")
            
            with st.expander("Show Explanation Log (XAI)"):
                st.write("This log shows the inference engine's reasoning process.")
                for entry in results['log']:
                    st.code(entry, language='text')
    else:
        st.info("Please adjust the sliders in the sidebar and click 'Analyze My Responses' to see your results.")

if __name__ == "__main__":
    main()
