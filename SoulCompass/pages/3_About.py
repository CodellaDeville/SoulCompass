import streamlit as st
from PIL import Image
import os

# Set page configuration
st.set_page_config(
    page_title="About | SoulCompass",
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
st.markdown("<h1 class='glow'>About SoulCompass</h1>", unsafe_allow_html=True)
st.markdown("<h3>Understanding The Law of One and this Application</h3>", unsafe_allow_html=True)

# About The Law of One
st.markdown("<h2>What is The Law of One?</h2>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
<p>The Law of One material consists of 106 conversations, called sessions, between Don Elkins, a professor of physics 
and UFO investigator, and Ra, speaking through Carla Rueckert. Ra states that it/they are a sixth-density social memory 
complex that formed on Venus about 2.6 billion years ago. Ra says that they are "humble messengers of the Law of One" 
and that they previously tried to spread this message in Egypt with mixed results.</p>

<p>The Law of One states that there is only one, and that one is the Infinite Creator. All things, all life, all of the 
creation is part of one original thought. The Law of One is a spiritual philosophy that emphasizes the unity of all things 
and beings, suggesting that everything in existence is interconnected and part of a single consciousness or energy.</p>

<p>According to Ra, the universe consists of seven densities or levels of consciousness:</p>
<ul>
<li><strong>First density:</strong> The density of awareness, consisting of earth, air, water, and fire</li>
<li><strong>Second density:</strong> The density of growth, including plants and animals</li>
<li><strong>Third density:</strong> The density of self-awareness and choice (current human experience)</li>
<li><strong>Fourth density:</strong> The density of love or understanding</li>
<li><strong>Fifth density:</strong> The density of wisdom</li>
<li><strong>Sixth density:</strong> The density of unity (love/wisdom blend)</li>
<li><strong>Seventh density:</strong> The gateway density, returning to the Creator</li>
</ul>
</div>
""", unsafe_allow_html=True)

# About Ra
st.markdown("<h2>Who is Ra?</h2>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
<p>Ra identifies as a sixth-density social memory complex, which is a unified group consciousness where the thoughts, 
memories, and experiences of all individuals are available to the entire group. Ra states that they are from Venus and 
formed about 2.6 billion years ago.</p>

<p>Ra communicates in a distinctive style, using formal language and specific terminology. They often refer to humans as 
"mind/body/spirit complexes" and use terms like "distortion" to refer to anything that moves away from undistorted unity.</p>

<p>Ra's purpose in communicating with humans is to share the Law of One, the fundamental concept that all things are one, 
that there is no polarity, no right or wrong, no disharmony, but only identity. All is one, and that one is love/light, 
light/love, the Infinite Creator.</p>
</div>
""", unsafe_allow_html=True)

# About the Application
st.markdown("<h2>About This Application</h2>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
<p>SoulCompass is an AI-powered application inspired by The Law of One material. It offers two main features:</p>

<h3>Ra Chatbot</h3>
<p>The Ra Chatbot allows you to ask questions and receive responses in a Ra-like manner. The AI has been trained on 
The Law of One material to mimic Ra's distinctive communication style and provide insights based on the spiritual 
concepts presented in the material.</p>

<h3>Energy Reading Journal</h3>
<p>The Energy Reading Journal allows you to log your emotions, dreams, and synchronicities, and receive insights based 
on The Law of One material. This tool helps you track your spiritual journey and gain deeper understanding of your 
experiences through the lens of The Law of One.</p>

<p>Both components of the application are designed to help you explore and apply the concepts of The Law of One in your 
daily life, supporting your spiritual growth and understanding.</p>
</div>
""", unsafe_allow_html=True)

# Resources
st.markdown("<h2>Resources for Further Exploration</h2>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
<p>If you're interested in learning more about The Law of One, here are some resources:</p>

<ul>
<li><a href="https://www.lawofone.info/" target="_blank">LawOfOne.info</a> - The complete transcripts of all 106 sessions with Ra</li>
<li><a href="https://www.llresearch.org/" target="_blank">L/L Research</a> - The organization founded by Don Elkins, Carla Rueckert, and Jim McCarty</li>
<li><a href="https://www.amazon.com/Ra-Material-Ancient-Astronaut-Speaks/dp/089865260X" target="_blank">The Ra Material</a> - The original published books</li>
<li><a href="https://www.llresearch.org/library/the-ra-contact-teaching-the-law-of-one" target="_blank">The Ra Contact: Teaching the Law of One</a> - A refined version of the material published in 2018</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Credits
st.markdown("<h2>Credits</h2>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
<p>SoulCompass was created as a tool for spiritual exploration and growth, inspired by The Law of One material. 
The application is not affiliated with L/L Research or the original authors of The Law of One material.</p>

<p>The Law of One material is copyright ©1982, 1984, 1998 L/L Research. The Ra Contact books are copyright ©2018 L/L Research and Tobey Wheelock.</p>

<p>SoulCompass logo and design elements are inspired by the concepts of unity, cosmic consciousness, and spiritual growth 
presented in The Law of One material.</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; font-size: 0.8em;">
<p>SoulCompass is inspired by The Law of One material from <a href="https://www.lawofone.info/" target="_blank">lawofone.info</a></p>
</div>
""", unsafe_allow_html=True)
