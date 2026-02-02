import streamlit as st

EMERGENCY_KEYWORDS = [
    "heart attack", "can't breathe", "cannot breathe", "stroke", 
    "unconscious", "bleeding", "severe chest pain", "blue lips",
    "seizure", "anaphylactic shock", "poisoning"
]

def check_emergency_keywords(text):
    """
    Checks text for emergency keywords.
    Returns True if emergency detected.
    """
    text = text.lower()
    for kw in EMERGENCY_KEYWORDS:
        if kw in text:
            return True
    return False

def render_emergency():
    st.markdown("### :material/emergency: Emergency Response & Safety Center")
    st.error("IF YOU ARE EXPERIENCING A LIFE-THREATENING EMERGENCY, CALL YOUR LOCAL EMERGENCY NUMBER (112/911/999) IMMEDIATELY.")

    tab1, tab2, tab3 = st.tabs(["⚡ Quick Action", "🩹 First Aid Guides", "💊 Medicine Safety"])

    with tab1:
        st.markdown("#### Real-time Keyword Detection")
        user_status = st.text_input("Describe current critical situation (for swift keyword check):")
        if user_status:
            if check_emergency_keywords(user_status):
                st.markdown("""
                <div class="medical-card pulse-animation" style="background: linear-gradient(135deg, #ff7675 0%, #d63031 100%); border-left: 5px solid #c0392b; color: white;">
                    <h3 style="color: white;">:material/warning: EMERGENCY DETECTED</h3>
                    <p><b>This sounds like a critical situation.</b></p>
                    <ul>
                        <li>🚑 Call Ambulance IMMEDIATELY</li>
                        <li>🚫 Do NOT drive yourself</li>
                        <li>🚪 Unlock front door for paramedics</li>
                        <li>📞 Stay on the line with emergency services</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("No immediate Red Flag keywords detected. However, trust your gut.")
        
        st.markdown("#### One-Tap Emergency Numbers")
        c1, c2, c3 = st.columns(3)
        c1.metric("Ambulance", "102/112")
        c2.metric("Police", "100/15")
        c3.metric("Fire", "101/16")

    with tab2:
        st.markdown("#### Common First Aid Procedures")
        choice = st.selectbox("Select Situation", ["CPR (Adult)", "Choking", "Severe Bleeding", "Burns"])
        
        if choice == "CPR (Adult)":
            st.info("1. Push hard and fast in the center of the chest.\n2. 100-120 compressions per minute.\n3. Push down at least 2 inches.")
        elif choice == "Choking":
            st.info("1. Perform Heimlich maneuver (abdominal thrusts).\n2. Stand behind and wrap arms around waist.\n3. Make a fist above navel.")
        elif choice == "Severe Bleeding":
            st.info("1. Apply direct pressure to wound using clean cloth.\n2. Elevate the injury if possible.\n3. If blood soaks through, add more layers (don't remove).")
        elif choice == "Burns":
            st.info("1. Cool the burn under cool running water for 10-20 minutes.\n2. Do NOT use ice.\n3. Cover with sterile gauze.")

    with tab3:
        st.markdown("#### Medicine Interaction & Safety")
        med1 = st.text_input("Medicine 1")
        med2 = st.text_input("Medicine 2 (Optional - Check Interaction)")
        
        if st.button("Check Safety Info", icon=":material/health_and_safety:"):
            st.warning(":material/warning: This is a simulation. Always ask your pharmacist.")
            if med1 and med2:
                st.markdown(f"**Potential Interaction between {med1} and {med2}:**")
                # Pseudo-logic for demo
                st.markdown("No severe known interactions in local database. *Verify with professional.*")
            elif med1:
                st.markdown(f"**General Info for {med1}:**")
                st.markdown("Take as directed. Report side effects like dizziness.")

