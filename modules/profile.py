import streamlit as st
import json
import os

import database as db

def render_profile():
    st.markdown("### :material/account_circle: Your Health Profile")
    email = st.session_state.get('user_email')
    
    # Load existing data
    current_data = db.get_user_profile(email)
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=current_data.get('name', ''))
            age = st.number_input("Age", min_value=0, max_value=120, value=current_data.get('age', 25))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(current_data.get('gender', 'Male')))
            blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], index=0)
        
        with col2:
            weight = st.number_input("Weight (kg)", value=current_data.get('weight', 70.0))
            height = st.number_input("Height (cm)", value=current_data.get('height', 170.0))
            allergies = st.text_area("Known Allergies", value=current_data.get('allergies', 'None'))
            chronic = st.text_area("Chronic Conditions", value=current_data.get('chronic', 'None'))

        submit = st.form_submit_button("Save Profile", icon=":material/save:")
        
        if submit:
            profile_data = {
                "name": name,
                "age": age,
                "gender": gender,
                "blood_type": blood_type,
                "weight": weight,
                "height": height,
                "allergies": allergies,
                "chronic": chronic
            }
            db.save_user_profile(email, profile_data)
            st.session_state['user_profile'] = profile_data
            st.success("Profile saved successfully!")

    st.markdown("---")
    st.markdown("#### :material/history: Medical History Log")
    st.info("Your chat history and symptom checks will be logged here.")
    
    if st.session_state.get('history'):
        with st.expander("View Recent Chat History"):
            for chat in st.session_state['history']:
                role = "You" if chat['role'] == "user" else "MediBot"
                st.write(f"**{role}:** {chat['content']}")
    else:
        st.write("No history available yet.")
