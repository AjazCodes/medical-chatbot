import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

def get_ai_symptom_analysis(symptoms, duration, severity, profile):
    """
    Generates an AI-powered symptom analysis using LangChain.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    provider = os.environ.get("API_PROVIDER", "Groq")
    
    if not api_key:
        return ":material/warning: API Key not found. Please ensure it's configured in the app."

    try:
        if provider == "Groq":
            llm = ChatOpenAI(
                temperature=0.3,
                openai_api_key=api_key,
                base_url="https://api.groq.com/openai/v1",
                model_name="llama-3.1-8b-instant"
            )
        else:
            llm = ChatOpenAI(temperature=0.3, openai_api_key=api_key, model_name="gpt-3.5-turbo")

        template = """You are an AI Medical Analyst. Analyze the following symptoms and provide a structured assessment.
        
        USER PROFILE:
        - Age/Gender: {age}/{gender}
        - Known Allergies: {allergies}
        - Chronic Conditions: {chronic}
        
        CURRENT SYMPTOMS:
        - Symptoms: {symptoms}
        - Duration: {duration} days
        - Severity: {severity}
        
        REQUIRED FORMAT (Markdown):
        ### :material/clinical_notes: Analysis Report
        1. **Possible Conditions:** List 2-3 likely conditions based on the symptoms and profile.
        2. **Risk Assessment:** (High/Medium/Low) based on symptoms and duration.
        3. **Personalized Explanation:** Why these match the user's symptoms and health history.
        4. **Recommended Next Steps:** (e.g., Home care, visit GP, Urgent care).
        
        SAFETY DISCLAIMER: Always end with a bold disclaimer that this is AI-generated and not a diagnosis.
        """
        
        prompt = PromptTemplate(
            input_variables=["age", "gender", "allergies", "chronic", "symptoms", "duration", "severity"],
            template=template
        )
        
        # Format profile data
        age = profile.get('age', 'N/A')
        gender = profile.get('gender', 'N/A')
        allergies = profile.get('allergies', 'None')
        chronic = profile.get('chronic', 'None')
        
        chain = prompt | llm
        response = chain.invoke({
            "age": age,
            "gender": gender,
            "allergies": allergies,
            "chronic": chronic,
            "symptoms": ", ".join(symptoms),
            "duration": duration,
            "severity": severity
        })
        
        return response.content

    except Exception as e:
        return f"Error analyzing symptoms: {str(e)}"

def clear_symptom_fields():
    """Callback to reset all symptom checker widgets."""
    st.session_state['symptom_selector'] = []
    st.session_state['duration_slider'] = 1
    st.session_state['severity_slider'] = "Mild"
    if 'latest_analysis' in st.session_state:
        del st.session_state['latest_analysis']

def render_symptom_checker():
    st.markdown("### :material/stethoscope: Intelligent Symptom Analysis")
    st.markdown("Get a personalized preliminary assessment based on your health profile and symptoms.")

    # Initialize widget keys in session state if not present
    if 'symptom_selector' not in st.session_state:
        st.session_state['symptom_selector'] = []
    if 'duration_slider' not in st.session_state:
        st.session_state['duration_slider'] = 1
    if 'severity_slider' not in st.session_state:
        st.session_state['severity_slider'] = "Mild"
    
    # Symptom Input
    all_symptoms = [
        "Fever", "Cough", "Fatigue", "Headache", "Nausea", 
        "Stomach Pain", "Chest Pain", "Shortness of Breath", 
        "Dizziness", "Rash", "Sore Throat", "Sensitivity to Light", 
        "Joint Pain", "Runny Nose", "Muscle Aches", "Loss of Taste/Smell"
    ]
    
    selected_symptoms = st.multiselect(
        "Search and Select Symptoms:", 
        all_symptoms,
        key="symptom_selector"
    )
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        duration = st.slider("How long have you had these symptoms? (Days)", 1, 30, key="duration_slider")
    with col2:
        severity = st.select_slider("Severity Level:", options=["Mild", "Moderate", "Severe", "Unbearable"], key="severity_slider")
    with col3:
        st.write("") # Spacer
        st.write("") # Spacer
        st.button("Clear", icon=":material/delete:", use_container_width=True, on_click=clear_symptom_fields)

    if st.button("Generate AI Analysis", icon=":material/search:", type="primary"):
        if not selected_symptoms:
            st.warning("Please select at least one symptom.")
            return

        with st.spinner("Analyzing your symptoms and health history..."):
            profile = st.session_state.get('user_profile', {})
            analysis = get_ai_symptom_analysis(selected_symptoms, duration, severity, profile)
            
            # Store in session state for reports
            st.session_state['latest_analysis'] = {
                "symptoms": selected_symptoms,
                "duration": duration,
                "severity": severity,
                "analysis": analysis
            }
            
            st.markdown('<div class="medical-card">', unsafe_allow_html=True)
            st.markdown(analysis)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Emergency Check Logic (Local fallback)
            emergency_keywords = ["chest pain", "shortness of breath", "dizziness", "unbearable"]
            if any(k in [s.lower() for s in selected_symptoms] for k in emergency_keywords) or severity == "Unbearable":
                st.error(":material/emergency: **POTENTIAL EMERGENCY:** Based on the severity or specific symptoms, please consider seeking immediate medical attention.")

            st.info(":material/info: Note: This AI assessment is for information only. Always consult a doctor for diagnosis and treatment.")
    
    # Show previous analysis if available
    elif 'latest_analysis' in st.session_state:
        analysis_data = st.session_state['latest_analysis']
        st.markdown("#### :material/history: Latest Analysis Result")
        st.markdown('<div class="medical-card">', unsafe_allow_html=True)
        st.markdown(analysis_data['analysis'])
        st.markdown('</div>', unsafe_allow_html=True)
