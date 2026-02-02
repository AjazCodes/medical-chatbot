import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationChain
from langchain_classic.prompts import PromptTemplate
import database as db

def get_chatbot_response(user_input, api_key, profile=None):
    """
    Generates a response from the medical chatbot using LangChain, aware of user profile.
    """
    if not api_key:
        return ":material/warning: Please enter your API Key in the sidebar to start the chat."

    try:
        # Determine Provider and Model
        import os
        provider = os.environ.get("API_PROVIDER", "Groq")
        
        if provider == "Groq":
            llm = ChatOpenAI(
                temperature=0.7,
                openai_api_key=api_key,
                base_url="https://api.groq.com/openai/v1",
                model_name="llama-3.1-8b-instant"
            )
        else:
            llm = ChatOpenAI(
                temperature=0.7,
                openai_api_key=api_key,
                model_name="gpt-3.5-turbo"
            )

        # Profile context
        gender = profile.get('gender', 'N/A') if profile else 'N/A'
        age = profile.get('age', 'N/A') if profile else 'N/A'
        allergies = profile.get('allergies', 'None') if profile else 'None'
        chronic = profile.get('chronic', 'None') if profile else 'None'

        # Prompt Template ensuring medical context
        template = f"""You are MediBot, a highly advanced and empathetic medical AI assistant. 
        Your goal is to provide helpful health information, explain symptoms, and offer general medical guidance.
        
        USER PROFILE:
        - Gender: {gender}
        - Age: {age}
        - Known Allergies: {allergies}
        - Chronic Conditions: {chronic}
        
        IMPORTANT RULES:
        1. ALWAYS state that you are an AI and NOT a doctor.
        2. DO NOT provide definitive diagnoses. Use phrases like "This could be indicative of...".
        3. ALWAYS recommend seeing a professional for serious concerns.
        4. Adjust your recommendations based on the user's Gender ({gender}) and Age ({age}). For example, if the user is female, consider relevant reproductive health or biological factors if applicable.
        5. Be concise, professional, and empathetic.
        
        Current conversation:
        {{history}}
        Human: {{input}}
        AI Assistant:"""

        PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

        # Memory Handling
        # We need to persist memory across streamlit reruns. 
        # Ideally, we store the 'memory' object in session_state, but LangChain memory objects 
        # can be tricky to pickle. A simpler way for a stateless web app is to just pass the 
        # history context manually or rebuild the chain. 
        # For simplicity in this demo, we will rely on Streamlit's session_state 'history' list 
        # to reconstruct context if needed, but here we'll use a fresh chain for the immediate response 
        # if we aren't maintaining a persistent chain object.
        
        # However, to be "Context Aware" as requested:
        if 'llm_chain' not in st.session_state:
             memory = ConversationBufferMemory(ai_prefix="AI Assistant")
             st.session_state['llm_chain'] = ConversationChain(
                llm=llm, 
                prompt=PROMPT, 
                verbose=True, 
                memory=memory
            )
        
        # Run the chain
        response = st.session_state['llm_chain'].predict(input=user_input)
        return response

    except Exception as e:
        return f"Error: {str(e)}. Please check your API usage or key."

def render_chatbot_interface(profile=None):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### :material/forum: Chat with MediBot")
    with col2:
        if st.button("Clear Chat", icon=":material/delete:", use_container_width=True):
            email = st.session_state.get('user_email')
            db.clear_chat_history(email)
            st.session_state['history'] = []
            if 'llm_chain' in st.session_state:
                st.session_state['llm_chain'].memory.clear()
            st.success("Chat history cleared!")
            st.rerun()
    
    # Check for API Key
    import os
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        st.warning(":material/key: Please enter your OpenAI/Groq API Key in the sidebar to enable the chatbot.")
        # Fallback Mock Mode for Demo purposes if no key provided
        st.info(":material/lightbulb: **Demo Mode Active:** API Key is missing, so I will respond with simulated answers.")
    
    # Display Chat History
    for chat in st.session_state['history']:
        if chat['role'] == 'user':
            st.markdown(f'<div class="user-message"><span class="material-symbols-rounded" style="vertical-align: middle; margin-right: 8px;">account_circle</span><b>You:</b> {chat["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message"><span class="material-symbols-rounded" style="vertical-align: middle; margin-right: 8px; color: #4FD1C5;">psychology</span><b>MediBot:</b> {chat["content"]}</div>', unsafe_allow_html=True)

    # Chat Input
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("Type your health question here...", key="user_input_field")
        submit_button = st.form_submit_button(label='Send Message', icon=":material/send:")

    if submit_button and user_input:
        email = st.session_state.get('user_email')
        # Add user message to history and DB
        st.session_state['history'].append({"role": "user", "content": user_input})
        db.save_chat_message(email, "user", user_input)
        
        # Get AI Response
        if api_key:
            response = get_chatbot_response(user_input, api_key, profile)
        else:
            # Mock Response
            import time
            time.sleep(1)
            response = "I am currently in Demo Mode. Please provide an API Key for real medical AI responses. Based on what you said (" + user_input + "), I would usually ask about duration and severity."
        
        # Add AI message to history and DB
        st.session_state['history'].append({"role": "assistant", "content": response})
        db.save_chat_message(email, "assistant", response)
        
        # Rerun to update the chat window
        st.rerun()
