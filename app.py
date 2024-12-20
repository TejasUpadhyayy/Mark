import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time

# Load environment variables
load_dotenv()

def initialize_genai():
    """Initialize the Gemini model with error handling"""
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("⚠️ Google API key not found. Please check your .env file.")
            st.stop()
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat()  # Removed history parameter
        return chat
    except Exception as e:
        st.error(f"⚠️ Error initializing Gemini: {str(e)}")
        st.stop()

def get_gemini_response(chat, question, temperature=0.7):
    """Get response from Gemini with streaming and error handling"""
    try:
        response = chat.send_message(
            question,
            generation_config={"temperature": temperature}
        )
        
        return response.text
    
    except Exception as e:
        st.error(f"⚠️ Error generating response: {str(e)}")
        return None

def create_sidebar():
    """Create sidebar with settings and information"""
    with st.sidebar:
        st.title("⚙️ Chat Settings")
        
        temperature = st.slider(
            "Creativity Level",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make responses more creative but potentially less focused"
        )
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
            
        st.divider()
        st.markdown("""
        ### About
        This is an enhanced chatbot powered by:
        - Google's Gemini Pro
        - Streamlit
        
        Made with 💖 by Your Name
        """)
        
        return temperature

# Page configuration
st.set_page_config(
    page_title="Enhanced Gemini Chat",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'chat' not in st.session_state:
    st.session_state['chat'] = initialize_genai()

# Main interface
st.title("🤖 Enhanced Gemini Chat")
st.markdown("---")

# Create sidebar and get temperature setting
temperature = create_sidebar()

# Display chat history with enhanced styling
for message in st.session_state.chat_history:
    role, text = message
    with st.chat_message(role, avatar="🧑‍💻" if role == "user" else "🤖"):
        st.markdown(f"**{text}**")

# Chat input and response
if prompt := st.chat_input("What's on your mind? Ask away..."):
    # Display user message
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(f"**{prompt}**")
    
    # Generate and display response
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤖 **Bot:** Thinking...")
        
        response = get_gemini_response(
            st.session_state.chat,
            prompt,
            temperature=temperature
        )
        
        if response:
            message_placeholder.markdown(f"🤖 **Bot:** {response}")
            # Update chat history
            st.session_state.chat_history.extend([
                ("user", prompt),
                ("assistant", response)
            ])