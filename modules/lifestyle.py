import streamlit as st
import random

def render_lifestyle():
    st.markdown("### :material/health_and_safety: Lifestyle & Mental Well-being")
    
    tab1, tab2 = st.tabs([":material/self_improvement: Healthy Living & Prevention", ":material/psychology: Mental Health Support"])
    
    with tab1:
        st.markdown("#### Personalized Recommendations")
        
        # Load profile context if available
        profile = st.session_state.get('user_profile', {})
        age = profile.get('age', 25)
        weight = profile.get('weight', 70)
        
        st.info(f"Generating insights for: Age {age}, Weight {weight}kg")
        
        # Recommendations based on gender
        gender = profile.get('gender', 'Male')
        
        col1, col2 = st.columns(2)
        with col1:
            if gender == "Female":
                diet_list = "<li>Iron-rich foods (spinach, lentils)</li><li>Calcium-rich dairy/alternatives</li><li>Hydration with electrolytes</li>"
            else:
                diet_list = "<li>High protein intake</li><li>Low sugar hydration</li><li>Green leafy vegetables</li>"
            
            st.markdown(f'<div class="medical-card"><h5>:material/restaurant: Diet Plan</h5><p>Based on your profile:</p><ul>{diet_list}</ul></div>', unsafe_allow_html=True)
        
        with col2:
            if gender == "Female":
                exercise_list = "<li>Pilates/Yoga for core strength</li><li>Moderate cardio (brisk walking)</li><li>Flexibility training</li>"
            else:
                exercise_list = "<li>30 mins Cardio (3x/week)</li><li>Strength training</li><li>High-intensity interval training</li>"
            
            st.markdown(f'<div class="medical-card"><h5>:material/directions_run: Exercise Tips</h5><p>Recommended Activity:</p><ul>{exercise_list}</ul></div>', unsafe_allow_html=True)
            
        st.markdown("#### Preventive Health Tracker")
        st.checkbox("Drank 8 glasses of water today?")
        st.checkbox("Took daily vitamins?")
        st.checkbox("Slept 7+ hours?")

    with tab2:
        st.markdown("#### Mental Health Screening (PHQ-2 / GAD-7 Simplified)")
        st.write("Over the last 2 weeks, how often have you been bothered by the following problems?")
        
        q1 = st.slider("1. Feeling nervous, anxious, or on edge?", 0, 3, 0, help="0: Not at all, 3: Nearly every day")
        q2 = st.slider("2. Not being able to stop or control worrying?", 0, 3, 0)
        
        score = q1 + q2
        if st.button("Check Score"):
            if score >= 3:
                st.warning(f"Your score is {score}/6. This suggests possible anxiety. Please consider talking to a professional.")
                st.markdown("[Find a Therapist Near You](https://www.google.com/maps/search/therapist)")
            else:
                st.success(f"Your score is {score}/6. You seem to be doing well!")
        
        st.markdown("#### 🧘 Relaxation Corner")
        if st.button("Start Breathing Exercise"):
            import time
            place = st.empty()
            with place.container():
                st.markdown("<h2 style='text-align: center;'>Breathe In... 🌬️</h2>", unsafe_allow_html=True)
                time.sleep(3)
                st.markdown("<h2 style='text-align: center;'>Hold... 😶</h2>", unsafe_allow_html=True)
                time.sleep(3)
                st.markdown("<h2 style='text-align: center;'>Breathe Out... 🌬️</h2>", unsafe_allow_html=True)
                time.sleep(3)
                st.markdown("<h2 style='text-align: center;'>Relaxed. 😌</h2>", unsafe_allow_html=True)
