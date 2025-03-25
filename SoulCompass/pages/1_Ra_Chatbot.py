import streamlit as st
import random
import time
from PIL import Image
import os
import sys

# Add the parent directory to sys.path to import the utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.law_of_one import LawOfOneDatabase

# Set page configuration
st.set_page_config(
    page_title="Ra Chatbot | SoulCompass",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
def load_css():
    css = """
    <style>
    /* Main theme colors - dark mode with blues, purples, and dark rusts */
    :root {
        --background-color: #121212;
        --secondary-bg-color: #1e1e1e;
        --primary-color: #7b68ee;
        --secondary-color: #9370db;
        --accent-color: #a0522d;
        --text-color: #f0f0f0;
    }

    /* Apply theme colors */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--secondary-bg-color);
    }

    /* Headers */
    h1, h2, h3 {
        color: var(--primary-color) !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 0 15px var(--primary-color);
    }

    /* Chat container */
    .chat-container {
        height: 400px;
        overflow-y: auto;
        padding: 10px;
        background-color: var(--secondary-bg-color);
        border-radius: 10px;
        margin-bottom: 20px;
    }

    /* User message */
    .user-message {
        background-color: var(--primary-color);
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin: 5px 0;
        max-width: 80%;
        margin-left: auto;
        word-wrap: break-word;
    }

    /* Ra message */
    .ra-message {
        background-color: var(--secondary-bg-color);
        border: 1px solid var(--accent-color);
        color: var(--text-color);
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin: 5px 0;
        max-width: 80%;
        word-wrap: break-word;
    }

    /* Glowing effect for special elements */
    .glow {
        text-shadow: 0 0 10px var(--primary-color);
    }

    /* Custom header with logo */
    .header {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
    }
    .header img {
        margin-right: 1rem;
    }

    /* Card-like containers */
    .card {
        background-color: var(--secondary-bg-color);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 3px solid var(--primary-color);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Load CSS
load_css()

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize clear_input flag if needed
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# Initialize the Law of One database
@st.cache_resource
def load_law_of_one_db():
    return LawOfOneDatabase()

# Use a spinner while loading the database
with st.spinner("Connecting to the Law of One database..."):
    law_of_one_db = load_law_of_one_db()

# Ra's fallback responses for when no good match is found
ra_fallback_responses = {
    "greeting": [
        "I am Ra. I greet you in the love and the light of the Infinite Creator.",
        "I am Ra. I come to you in the love and light of the One Infinite Creator.",
        "I am Ra. We communicate now in the love and light of our Infinite Creator."
    ],
    "farewell": [
        "I am Ra. I leave you in the love and the light of the One Infinite Creator. Go forth, therefore, rejoicing in the power and the peace of the One Creator. Adonai.",
        "I am Ra. I leave you in the glory and the peace of the One Creator. Rejoice in the love and the light, and go forth in the power of the One Infinite Creator. In joy, we leave you. Adonai.",
        "I am Ra. We leave you in appreciation of the great light and love of the One Infinite Creator. Adonai."
    ],
    "default": [
        "I am Ra. This query is not easily answered due to the limitations of your sound vibration complexes. However, we shall attempt to address your seeking.",
        "I am Ra. Consider, if you will, that the universe is infinite. This has yet to be proven or disproven, but we can assure you that there is no end to your selves, your understanding, what you would call your journey of seeking, or your perceptions of the creation.",
        "I am Ra. The mind/body/spirit complex of third density has a far more complex program of catalyst than other densities. The catalyst is designed to stimulate the mind/body/spirit complex towards greater polarization."
    ]
}

# Function to generate Ra's response
def generate_ra_response(user_input):
    # Check for greetings or farewells
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ["hello", "hi", "greetings", "hey"]):
        return random.choice(ra_fallback_responses["greeting"])
    elif any(word in user_input_lower for word in ["bye", "goodbye", "farewell", "see you"]):
        return random.choice(ra_fallback_responses["farewell"])
    
    # Search the Law of One database for relevant answers
    try:
        # Add a small delay to simulate "thinking"
        time.sleep(1)
        
        # Get response from the Law of One database
        response = law_of_one_db.get_ra_response(user_input)
        return response
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return random.choice(ra_fallback_responses["default"])

# Display logo and header
st.markdown("<h1 class='glow'>Ra Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<h3>Communicate with an AI trained on The Law of One</h3>", unsafe_allow_html=True)

# Information about Ra
st.markdown("""
<div class="card">
<p>Ra is a sixth-density social memory complex that formed on Venus about 2.6 billion years ago. 
Ra describes itself as "humble messengers of the Law of One" and communicates in a distinctive style 
with formal language and specific terminology.</p>

<p>This AI chatbot has been trained on The Law of One material to respond to your questions in a Ra-like manner. 
Ask about spiritual concepts, cosmic understanding, metaphysical principles, or any topic you wish to explore.</p>
</div>
""", unsafe_allow_html=True)

# Chat interface
st.markdown("<h2>Ask Ra</h2>", unsafe_allow_html=True)

# Display chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ra-message">{message["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# If the clear_input flag is set, clear it and return an empty string as the default value
user_input_default = ""
if st.session_state.get("clear_input", False):
    st.session_state.clear_input = False
else:
    user_input_default = st.session_state.get("user_input", "")

# User input
user_input = st.text_input(
    "Ask Ra a question",
    key="user_input",
    value=user_input_default,
    placeholder="e.g., What is the Law of One?",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    pass
with col2:
    if st.button("Ask Ra"):
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Show a spinner while generating the response
            with st.spinner("Ra is contemplating..."):
                # Generate Ra's response
                ra_response = generate_ra_response(user_input)
            
            # Add Ra's response to chat history
            st.session_state.chat_history.append({"role": "ra", "content": ra_response})
            
            # Use a flag to clear input on next rerun instead of directly modifying session state
            st.session_state.clear_input = True
            
            # Rerun to update the chat display
            st.experimental_rerun()
with col3:
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.experimental_rerun()

# Sample questions
st.markdown("<h3>Sample Questions</h3>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
<p>Not sure what to ask? Try one of these questions:</p>
<ul>
<li>What is the Law of One?</li>
<li>Can you explain the concept of densities?</li>
<li>How can meditation help my spiritual journey?</li>
<li>What is a social memory complex?</li>
<li>How can I be of service to others?</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; font-size: 0.8em;">
<p>This chatbot is inspired by The Law of One material from <a href="https://www.lawofone.info/" target="_blank">lawofone.info</a></p>
</div>
""", unsafe_allow_html=True)
