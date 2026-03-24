 AI Medical Chatbot App

An intelligent AI-powered Medical Chatbot that provides real-time responses to user health-related queries, offers symptom-based guidance, and enhances user experience with a clean, interactive interface.
Live Demo

https://medical-chatbot-qpgqn2ezasyep3jvr5v46c.streamlit.app/

Project Overview

This project is designed to simulate a virtual medical assistant that helps users understand basic symptoms and health concerns using AI.

It integrates modern AI APIs to deliver fast, conversational, and context-aware responses while maintaining a simple and user-friendly interface.

Key Features
AI-powered chatbot for medical queries
Real-time interactive chat
Smart symptom-based suggestions
Clean and responsive UI/UX
Fast performance using Streamlit
Secure API key handling with .env
Accessible across devices
Tech Stack
Category	Technologies Used
Frontend -> Streamlit UI
Backend ->	Python
AI Model ->	OpenAI / Gemini / Groq API
Environment ->	Python, Virtual Environment
Deployment	-> Streamlit Cloud
Folder Structure
medical-chatbot/
│── app.py                # Main application file
│── requirements.txt     # Dependencies
│── .env                 # API keys (not pushed to GitHub)
│── assets/              # Images / UI resources
│── README.md            # Project documentation
 Installation & Setup Guide
1️⃣ Clone Repository
git clone (your repository)
cd medical-chatbot
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # For Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Add API Key

Create a .env file:

API_KEY=your_api_key_here
Make sure .env is added to .gitignore

5️⃣ Run the App
streamlit run app.py
 How It Works
User enters a medical-related query
Query is sent to AI API
AI processes input using NLP
Response is displayed instantly in chat UI

Future Enhancements
-> Voice-based interaction
-> Multi-language support
-> Health report generation
-> Doctor consultation integration
-> Advanced symptom prediction
Disclaimer

This application is for educational purposes only and does not provide medical diagnosis. Always consult a licensed healthcare professional.

 License

Licensed under the MIT License
