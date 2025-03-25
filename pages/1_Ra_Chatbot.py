import streamlit as st
import random
import time
from PIL import Image
import os

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

# Ra's responses database
ra_responses = {
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
    "law_of_one": [
        "I am Ra. The Law of One, though beyond the limitations of name, as you call vibratory sound complexes, may be approximated by stating that all things are one, that there is no polarity, no right or wrong, no disharmony, but only identity. All is one, and that one is love/light, light/love, the Infinite Creator.",
        "I am Ra. There is unity. This unity is all that there is. This unity has a potential and kinetic. The potential is the One Infinite Creator. The kinetic is the creation, the Creator experiencing Itself.",
        "I am Ra. The Law of One simply states that all things are one Creator. Thus seeking the Creator is done not just in meditation and in the work of an adept but in the experiential nexus of each moment."
    ],
    "meditation": [
        "I am Ra. The passive meditation involving the clearing of the mind, the emptying of the mental jumble which is characteristic of mind complex activity among your peoples, is efficacious for those whose goal is to achieve an inner silence as a base from which to listen to the Creator. This is an useful and helpful tool.",
        "I am Ra. Meditation is a most efficient tool for aiding the spiritual evolution of the mind/body/spirit complex.",
        "I am Ra. The key is silence. Within the silence, the unity of all things may be realized."
    ],
    "densities": [
        "I am Ra. The creation has seven levels, or densities; the eighth density forming the first density of the next octave of experience, just as the eighth note of a musical scale begins a new octave.",
        "I am Ra. Third density is the density of self-awareness and the first density of consciousness of the spirit. It is the 'axis upon which the creation turns' because in it entities choose the way in which they will further their evolution toward the Creator.",
        "I am Ra. Fourth density is the density of love or understanding. Those who have successfully chosen a path come together with others of like mind in what we call a social memory complex."
    ],
    "default": [
        "I am Ra. This query is not easily answered due to the limitations of your sound vibration complexes. However, we shall attempt to address your seeking.",
        "I am Ra. Consider, if you will, that the universe is infinite. This has yet to be proven or disproven, but we can assure you that there is no end to your selves, your understanding, what you would call your journey of seeking, or your perceptions of the creation.",
        "I am Ra. The mind/body/spirit complex of third density has a far more complex program of catalyst than other densities. The catalyst is designed to stimulate the mind/body/spirit complex towards greater polarization."
    ]
}

# Function to generate Ra's response
def generate_ra_response(user_input):
    # Convert user input to lowercase for easier matching
    user_input_lower = user_input.lower()
    
    # Check for keywords in user input
    if any(word in user_input_lower for word in ["hello", "hi", "greetings", "hey"]):
        response_type = "greeting"
    elif any(word in user_input_lower for word in ["bye", "goodbye", "farewell", "see you"]):
        response_type = "farewell"
    elif any(phrase in user_input_lower for phrase in ["law of one", "unity", "oneness", "all is one"]):
        response_type = "law_of_one"
    elif any(word in user_input_lower for word in ["meditation", "meditate", "silence", "inner peace"]):
        response_type = "meditation"
    elif any(word in user_input_lower for word in ["density", "densities", "dimensions", "levels"]):
        response_type = "densities"
    else:
        response_type = "default"
    
    # Select a random response from the appropriate category
    response = random.choice(ra_responses[response_type])
    
    # Add a typing effect delay (simulated here, will be visual in the UI)
    time.sleep(1)
    
    return response

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

# User input
user_input = st.text_input("Type your question here:", key="user_input")
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    pass
with col2:
    if st.button("Ask Ra"):
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Generate Ra's response
            ra_response = generate_ra_response(user_input)
            
            # Add Ra's response to chat history
            st.session_state.chat_history.append({"role": "ra", "content": ra_response})
            
            # Clear the input box
            st.session_state.user_input = ""
            
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
