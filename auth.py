import streamlit as st
import database as db

def render_login_signup():
    # The CSS is already loaded by app.py's load_css()
    # We just need to make sure we don't add any extra st.markdown calls that create space
    st.markdown('<div class="main-auth-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="auth-logo">🏥</div>', unsafe_allow_html=True)
        st.markdown('<h2 class="auth-title">MediBot Pro</h2>', unsafe_allow_html=True)
        
        # Theme toggle on login page
        t_col1, t_col2, t_col3 = st.columns([1, 2, 1])
        with t_col2:
            theme = st.toggle("🌙 Dark Mode", value=(st.session_state['theme'] == 'Dark'), key="login_theme")
            st.session_state['theme'] = 'Dark' if theme else 'Light'

        email = st.text_input("Email", placeholder="Enter your email", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
        
        if st.session_state.get('auth_mode') == 'Signup':
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
            if st.button("Create Account ✨", use_container_width=True):
                if not email or not password:
                    st.error("Please fill all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    if db.add_user(email, password):
                        st.success("Account created! Welcome to MediBot.")
                        st.session_state['auth_mode'] = 'Login'
                        st.rerun()
                    else:
                        st.error("This email is already registered.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="secondary-btn" style="margin-top: 0.5rem;">', unsafe_allow_html=True)
            if st.button("Already have an account? Log In", use_container_width=True):
                st.session_state['auth_mode'] = 'Login'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
                
        else:
            st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
            if st.button("Log In 🚀", use_container_width=True):
                if db.verify_user(email, password):
                    st.session_state['authenticated'] = True
                    st.session_state['user_email'] = email
                    st.session_state['user_profile'] = db.get_user_profile(email)
                    st.session_state['history'] = db.get_chat_history(email)
                    st.rerun()
                else:
                    st.error("Invalid email or password. Please try again.")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="secondary-btn" style="margin-top: 0.5rem;">', unsafe_allow_html=True)
            if st.button("Don't have an account? Sign Up", use_container_width=True):
                st.session_state['auth_mode'] = 'Signup'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) # Close auth-wrapper
    st.markdown('</div>', unsafe_allow_html=True) # Close main-auth-container

def logout():
    st.session_state['authenticated'] = False
    st.session_state['user_email'] = None
    st.session_state['user_profile'] = {}
    st.session_state['history'] = []
    if 'llm_chain' in st.session_state:
        del st.session_state['llm_chain']
    if 'current_page' in st.session_state:
        st.session_state['current_page'] = '🏠 Home'
    st.rerun()
