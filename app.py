import streamlit as st
import os
import sys
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to sys.path to ensure modules are found
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import Modules at top level
try:
    from modules.chatbot import render_chatbot_interface
    from modules.symptoms import render_symptom_checker
    from modules.emergency import render_emergency
    from modules.profile import render_profile
    from modules.lifestyle import render_lifestyle
    from modules.reports import render_reports
    import auth
    import database as db
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.info("Ensure the 'modules' folder and '__init__.py' exist in your project root.")

# Page Config (Must be first)
st.set_page_config(
    page_title="MediBot - AI Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- USER CONFIGURATION ---
# The API Key is now loaded from the .env file for security.
MANUAL_API_KEY = os.getenv("GROQ_API_KEY", "")  
MANUAL_PROVIDER = "Groq" 

# Auto-Load Configuration into Environment (Crucial for Deployment)
if MANUAL_API_KEY:
    os.environ['OPENAI_API_KEY'] = MANUAL_API_KEY
    os.environ['API_PROVIDER'] = MANUAL_PROVIDER
# --------------------------

# Initialize Session State (Must be early)
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'user_profile' not in st.session_state:
    st.session_state['user_profile'] = {}
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = None
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'Light'

def get_css_content():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path, encoding='utf-8') as f:
            return f.read()
    return ""

def load_css():
    try:
        css_content = get_css_content()
        theme = st.session_state.get('theme', 'Light')
        if theme == 'Dark':
            theme_vars = """
                :root {
                    --bg-main: #0B0E14; --bg-card: #151921; --sidebar-bg: #151921;
                    --text-main: #F8FAFC; --text-muted: #94A3B8; --heading-color: #F8FAFC;
                    --border-color: #2D3748; --shadow-main: 0 10px 40px rgba(0,0,0,0.6);
                    --input-bg: #1A202C; --bot-msg-bg: #1A202C;
                    --primary-gradient: linear-gradient(135deg, #818CF8 0%, #C084FC 100%);
                }
            """
        else:
            theme_vars = """
                :root {
                    --bg-main: #FFFFFF; --bg-card: #FFFFFF; --sidebar-bg: #F8FAFC;
                    --text-main: #0F172A; --text-muted: #475569; --heading-color: #1E293B;
                    --border-color: #E2E8F0; --shadow-main: 0 10px 25px rgba(0,0,0,0.05);
                    --input-bg: #FFFFFF; --bot-msg-bg: #F1F5F9;
                    --primary-gradient: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
                }
            """
        st.markdown(f'<style>{theme_vars}\n{css_content}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading CSS: {e}")

# Import Modules (We will create these next)
# To prevent errors before files exist, we'll try/except or just define placeholder functions here for now
# Ideally, we build the files, but for the skeleton, I'll set up the routing.


# --- ICON HELPER ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_nav_button(label, key, icon):
    """Renders a simple, stable sidebar navigation button with Material Symbols."""
    if st.sidebar.button(label, key=key, icon=icon, use_container_width=True):
        st.session_state['current_page'] = label
        st.rerun()

# Main App Logic (Auth Check)
if not st.session_state['authenticated']:
    load_css() # Load CSS for login page too
    auth.render_login_signup()
else:
    # Sidebar Navigation
    with st.sidebar:
        st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
        st.title("🏥 MediBot Pro")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Theme Toggle
        theme = st.toggle("🌙 Dark Mode", value=(st.session_state['theme'] == 'Dark'))
        st.session_state['theme'] = 'Dark' if theme else 'Light'
        
        # Load CSS AFTER theme toggle for immediate update
        load_css()
        
        st.markdown(f"**User:** {st.session_state['user_email']}")
        if st.sidebar.button("🚪 Logout", key="logout_btn", use_container_width=True):
            auth.logout()
        
        st.markdown("---")
        
        # Initialize page state
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = 'Home'
        
        # Navigation buttons
        st.markdown("### Navigation")
        
        render_nav_button("Home", "nav_home", ":material/dashboard:")
        render_nav_button("AI Chatbot", "nav_chatbot", ":material/psychology:")
        render_nav_button("Symptom Checker", "nav_symptoms", ":material/stethoscope:")
        render_nav_button("Emergency", "nav_emergency", ":material/emergency:")
        render_nav_button("User Profile", "nav_profile", ":material/account_circle:")
        render_nav_button("Lifestyle & Mental Health", "nav_lifestyle", ":material/health_and_safety:")
        render_nav_button("Reports", "nav_reports", ":material/analytics:")
        render_nav_button("About", "nav_about", ":material/info:")
        
        st.markdown("---")
        
        
        st.markdown("---")
        st.info("💡 **Tip:** Use the 'Emergency' tab for urgent keyword checks.")

    # Get current selection
    selection = st.session_state.get("current_page", "Home")

    # Routing
    if selection == "Home":
        st.title("Welcome to MediBot 🩺")
        
        # Premium 3D Feature Cards
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        
        def render_feature_card(title, description, icon_name):
            icon_path = os.path.join(assets_dir, f"{icon_name}.png")
            icon_html = ""
            if os.path.exists(icon_path):
                img_base64 = get_base64_of_bin_file(icon_path)
                icon_html = f'<img src="data:image/png;base64,{img_base64}" class="feature-icon-3d">'
            
            st.markdown(f"""
            <div class="feature-card">
                {icon_html}
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            render_feature_card("AI Medical Chat", "Ask anything about symptoms, medicines, and wellness.", "chatbot")
        with col2:
            render_feature_card("Symptom Checker", "Analyze your condition with AI-driven diagnosis.", "symptoms")
        with col3:
            render_feature_card("Your Health Hub", "Manage your profile, reports, and lifestyle.", "home")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_start1, col_start2 = st.columns(2)
        with col_start1:
            st.markdown("""
            <div class="medical-card">
                <h4>🚀 Quick Start</h4>
                <p>Go to the <b>User Profile</b> tab to set up your health details for personalized advice.</p>
            </div>
            """, unsafe_allow_html=True)
        with col_start2:
            st.warning("⚠️ **Disclaimer:** MediBot is an AI assistant and NOT a doctor. Always seek professional medical advice for serious conditions.")

    elif selection == "AI Chatbot":
        st.title(":material/psychology: AI Medical Chat")
        profile = st.session_state.get('user_profile', {})
        render_chatbot_interface(profile)

    elif selection == "Symptom Checker":
        st.title(":material/stethoscope: Symptom Analysis")
        render_symptom_checker()

    elif selection == "Emergency":
        st.title(":material/emergency: Emergency & First Aid")
        render_emergency()

    elif selection == "User Profile":
        st.title(":material/account_circle: Your Health Profile")
        render_profile()

    elif selection == "Lifestyle & Mental Health":
        st.title(":material/health_and_safety: Lifestyle & Mental Health")
        render_lifestyle()

    elif selection == "Reports":
        st.title(":material/analytics: Medical Reports")
        render_reports()

    elif selection == "About":
        st.title(":material/info: About MediBot")
        st.markdown("""
        <div class="medical-card">
            <p>Developed for an Advanced Medical Chatbot Project.</p>
            <p><b>Tech Stack:</b> Python, Streamlit, LangChain, OpenAI/Groq.</p>
            <p><b>Version:</b> 1.0.0</p>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<center class='footer'>&copy; 2026 MediBot AI. All rights reserved.</center>", unsafe_allow_html=True)
