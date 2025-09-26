# app.py
# The main application file for the Mental Health Support Expert System.
import numpy as np
import streamlit as st
from knowledge_base import SYMPTOMS
from inference_engine import InferenceEngine
from fuzzy_engine import create_fuzzy_control_system, calculate_concern_level

def initialize_session_state():
    """Initializes variables in Streamlit's session state."""
    if 'stage' not in st.session_state:
        st.session_state.stage = 'intro'
    if 'symptom_keys' not in st.session_state:
        st.session_state.symptom_keys = list(SYMPTOMS.keys())
    if 'current_symptom_index' not in st.session_state:
        st.session_state.current_symptom_index = 0
    if 'engine' not in st.session_state:
        st.session_state.engine = InferenceEngine()
    if 'fuzzy_system' not in st.session_state:
        st.session_state.fuzzy_system = create_fuzzy_control_system()
    if 'results' not in st.session_state:
        st.session_state.results = None

def main():
    """Main function to run the Streamlit application."""
    initialize_session_state()

    st.set_page_config(page_title="Mental Wellness Assistant", layout="centered")

    # --- UI Styling for a Calmer Experience ---
    st.markdown("""
        <style>
       .stApp {
            background-color: #F0F2F6;
        }
       .st-emotion-cache-16txtl3 {
            padding: 2rem 1rem 10rem;
        }
       .stButton>button {
            border-radius: 20px;
            border: 1px solid #4A90E2;
            background-color: #FFFFFF;
            color: #4A90E2;
        }
       .stButton>button:hover {
            border: 1px solid #357ABD;
            background-color: #F0F8FF;
            color: #357ABD;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Mental Wellness Assistant")

    if st.session_state.stage == 'intro':
        st.info("**Disclaimer:** This is an educational tool and not a substitute for professional medical advice. If you are in crisis, please contact a helpline or emergency services immediately.", icon="⚠️")
        st.write("Hello! I'm here to help you reflect on your well-being. We'll go through a few questions together. Your responses are not stored after you close this window.")
        if st.button("Let's Begin"):
            st.session_state.stage = 'assessment'
            st.rerun()

    elif st.session_state.stage == 'assessment':
        idx = st.session_state.current_symptom_index
        if idx < len(st.session_state.symptom_keys):
            symptom_key = st.session_state.symptom_keys[idx]
            symptom_info = SYMPTOMS[symptom_key]
            
            st.write(f"**Question {idx + 1}/{len(st.session_state.symptom_keys)}**")
            st.write(symptom_info['question'])
            
            severity = st.slider("On a scale of 0 (Not at all) to 10 (Extremely), how much has this affected you?", 0, 10, 0, key=f"slider_{symptom_key}")

            if st.button("Next Question", key=f"btn_{symptom_key}"):
                if severity > 0:
                    st.session_state.engine.add_fact(symptom_key, severity)
                st.session_state.current_symptom_index += 1
                st.rerun()
        else:
            st.session_state.stage = 'calculating'
            st.rerun()

    elif st.session_state.stage == 'calculating':
        with st.spinner("Analyzing your responses..."):
            # Run Inference Engine
            detected, interventions, log = st.session_state.engine.run()
            
            # Calculate Fuzzy Concern Level
            reported_severities = list(st.session_state.engine.facts.values())
            avg_severity = np.mean(reported_severities) if reported_severities else 0
            symptom_count = len(reported_severities)
            concern_score = calculate_concern_level(st.session_state.fuzzy_system, avg_severity, symptom_count)
            
            st.session_state.results = {
                "detected": detected,
                "interventions": interventions,
                "log": log,
                "concern_score": concern_score
            }
            st.session_state.stage = 'summary'
            st.rerun()

    elif st.session_state.stage == 'summary':
        results = st.session_state.results
        
        st.header("Your Wellness Summary")
        
        st.progress(int(results['concern_score']), text=f"Overall Concern Level: {int(results['concern_score'])}/100")
        st.write("This score is calculated based on the number and severity of the symptoms you reported. It is an indicator for reflection, not a diagnosis.")

        if not results['detected']:
            st.success("Based on your responses, no specific patterns of concern were strongly indicated. It's always great to be proactive about your mental well-being!")
        else:
            st.subheader("Potential Patterns for Reflection:")
            for condition in results['detected']:
                with st.container(border=True):
                    st.markdown(f"**{condition['name']}**")
                    st.write(condition['explanation'])

        if results['interventions']:
            st.subheader("Suggested Self-Help Strategies:")
            for name, desc in results['interventions'].items():
                with st.expander(f"Learn about: **{name}**"):
                    st.write(desc)
        
        # XAI Component
        with st.expander("How was this summary generated? (Explainable AI)"):
            st.write("This summary was generated by an expert system that analyzed your responses using a set of rules based on clinical guidelines.")
            st.write("The following reasoning steps were part of the process:")
            for log_entry in results['log']:
                st.text(f"- {log_entry}")
            st.write(f"A fuzzy logic system then calculated the overall concern score based on an average symptom severity of {np.mean(list(st.session_state.engine.facts.values())):.1f} and a count of {len(st.session_state.engine.facts)} reported symptoms.")

        if st.button("Start Over"):
            # Reset the session state completely
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":

    main()
