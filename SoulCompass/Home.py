import streamlit as st
from PIL import Image
import os

# Set page configuration
st.set_page_config(
    page_title="SoulCompass: AI-Powered Channeled Insights",
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

    /* Card-like containers */
    .card {
        background-color: var(--secondary-bg-color);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 3px solid var(--primary-color);
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
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Load CSS
load_css()

# Display logo and header
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(logo, width=150)
    with col2:
        st.markdown("<h1 class='glow'>SoulCompass</h1>", unsafe_allow_html=True)
        st.markdown("<h3>AI-Powered Channeled Insights</h3>", unsafe_allow_html=True)
else:
    st.markdown("<h1 class='glow'>SoulCompass</h1>", unsafe_allow_html=True)
    st.markdown("<h3>AI-Powered Channeled Insights</h3>", unsafe_allow_html=True)

# Introduction
st.markdown("""
<div class="card">
<p>Welcome to SoulCompass, an application inspired by The Law of One material. 
This tool offers two primary features to support your spiritual journey:</p>
</div>
""", unsafe_allow_html=True)

# Feature cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
    <h2>Ra Chatbot</h2>
    <p>Engage with an AI trained on The Law of One that responds to your questions in a Ra-like manner. 
    Explore spiritual concepts, cosmic understanding, and metaphysical principles through conversation.</p>
    </div>
    """, unsafe_allow_html=True)
    st.button("Ask Ra a Question", key="ra_button")

with col2:
    st.markdown("""
    <div class="card">
    <h2>Energy Reading Journal</h2>
    <p>Log your emotions, dreams, and synchronicities to receive insights based on The Law of One material. 
    Track your spiritual journey and gain deeper understanding of your experiences.</p>
    </div>
    """, unsafe_allow_html=True)
    st.button("Start Journaling", key="journal_button")

# About The Law of One
st.markdown("""
<div class="card">
<h2>About The Law of One</h2>
<p>The Law of One material consists of 106 conversations, called sessions, between Don Elkins, a professor of physics 
and UFO investigator, and Ra, speaking through Carla Rueckert. Ra states that it/they are a sixth-density social memory 
complex that formed on Venus about 2.6 billion years ago. Ra says that they are "humble messengers of the Law of One" 
and that they previously tried to spread this message in Egypt with mixed results.</p>

<p>The Law of One states that there is only one, and that one is the Infinite Creator. All things, all life, all of the 
creation is part of one original thought. The Law of One is a spiritual philosophy that emphasizes the unity of all things 
and beings, suggesting that everything in existence is interconnected and part of a single consciousness or energy.</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; font-size: 0.8em;">
<p>SoulCompass is inspired by The Law of One material from <a href="https://www.lawofone.info/" target="_blank">lawofone.info</a></p>
</div>
""", unsafe_allow_html=True)
