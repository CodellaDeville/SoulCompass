import streamlit as st
import pandas as pd
import datetime
import random
import os
import sys
from PIL import Image

# Add the parent directory to sys.path to import the utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.law_of_one import LawOfOneDatabase

# Set page configuration
st.set_page_config(
    page_title="Energy Reading Journal | SoulCompass",
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

    /* Journal entry */
    .journal-entry {
        background-color: var(--secondary-bg-color);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 3px solid var(--accent-color);
    }

    /* Insight box */
    .insight-box {
        background-color: rgba(123, 104, 238, 0.2);
        border: 1px solid var(--primary-color);
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
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

# Initialize session state for journal entries if it doesn't exist
if 'journal_entries' not in st.session_state:
    st.session_state.journal_entries = []

# Initialize form clearing flags
if 'clear_emotion_form' not in st.session_state:
    st.session_state.clear_emotion_form = False
if 'clear_dream_form' not in st.session_state:
    st.session_state.clear_dream_form = False
if 'clear_sync_form' not in st.session_state:
    st.session_state.clear_sync_form = False

# Initialize the Law of One database
@st.cache_resource
def load_law_of_one_db():
    return LawOfOneDatabase()

# Use a spinner while loading the database
with st.spinner("Connecting to the Law of One database..."):
    law_of_one_db = load_law_of_one_db()

# Fallback insights if database search fails
fallback_insights = {
    "emotions": [
        "I am Ra. The emotions you are experiencing are catalysts for spiritual growth. Remember that all is one, and these feelings are part of the Creator experiencing itself.",
        "I am Ra. Your emotional state is a distortion of the One Infinite Creator. By accepting and balancing these emotions, you move closer to understanding the Law of One.",
        "I am Ra. The emotions you describe are vibrations that can be balanced through meditation and contemplation. As you balance these energies, you open pathways to intelligent infinity."
    ],
    "dreams": [
        "I am Ra. The dream state offers access to the deeper portions of the mind complex, where symbols and archetypes reside. Your dream contains symbols that reflect your current spiritual journey.",
        "I am Ra. Dreams often serve as a bridge between your conscious mind and the cosmic mind. The imagery you describe suggests communication from your higher self regarding your spiritual path.",
        "I am Ra. In the dream state, the veil between densities thins, allowing glimpses of other realities and potentials."
    ],
    "synchronicities": [
        "I am Ra. What you call synchronicity is often the higher self communicating through the illusion of space/time. These patterns indicate alignment with your spiritual purpose.",
        "I am Ra. Synchronicities are moments when the veil thins, allowing you to perceive the interconnectedness of all things. They often appear when you are moving in harmony with your pre-incarnative choices.",
        "I am Ra. The meaningful coincidences you describe are manifestations of the Law of One in action."
    ]
}

# Function to generate insights based on journal entry
def generate_insight(entry_type, entry_text):
    try:
        # First, try to get a relevant response from the Law of One database
        if entry_type == "emotions":
            search_query = f"emotions {entry_text}"
        elif entry_type == "dreams":
            search_query = f"dreams {entry_text}"
        elif entry_type == "synchronicities":
            search_query = f"synchronicity {entry_text}"
        
        # Search the database
        results = law_of_one_db.search(search_query)
        
        if results:
            # Use the most relevant answer
            best_match = results[0]
            insight = best_match['answer']
            
            # Add a source reference
            source_ref = f"\n\n[From Session {best_match['session_id']}]"
            
            # Ensure it starts with Ra's greeting if it doesn't already
            if not insight.startswith("I am Ra"):
                insight = "I am Ra. " + insight
                
            # Add personalized elements based on the entry text
            if "challenge" in entry_text.lower() or "difficult" in entry_text.lower():
                personalized = " The challenges you face are opportunities for polarization and growth toward the Creator."
            elif "joy" in entry_text.lower() or "happy" in entry_text.lower():
                personalized = " Your experience of joy is a glimpse of the true nature of the Creator, which is infinite love and light."
            elif "confused" in entry_text.lower() or "uncertain" in entry_text.lower():
                personalized = " Confusion is often a precursor to understanding. Sit with this catalyst and allow it to transform within you."
            elif "meditation" in entry_text.lower():
                personalized = " Your meditation practice strengthens your connection to intelligent infinity and accelerates your spiritual evolution."
            else:
                personalized = " Remember that you are on a unique path of seeking, and each experience brings you closer to understanding the Law of One."
            
            return insight + personalized + source_ref
        else:
            # Use fallback if no relevant results found
            return random.choice(fallback_insights[entry_type])
    except Exception as e:
        st.error(f"Error generating insight: {e}")
        return random.choice(fallback_insights[entry_type])

# Display logo and header
st.markdown("<h1 class='glow'>Energy Reading Journal</h1>", unsafe_allow_html=True)
st.markdown("<h3>Log your experiences and receive insights based on The Law of One</h3>", unsafe_allow_html=True)

# Information about the journal
st.markdown("""
<div class="card">
<p>This Energy Reading Journal allows you to log your emotions, dreams, and synchronicities, 
and receive insights based on The Law of One material. Regular journaling can help you identify 
patterns in your spiritual journey and deepen your understanding of your experiences.</p>

<p>The insights provided are generated based on Ra's teachings about how our daily experiences 
serve as catalysts for spiritual growth and evolution.</p>
</div>
""", unsafe_allow_html=True)

# Journal interface
st.markdown("<h2>New Journal Entry</h2>", unsafe_allow_html=True)

# Create tabs for different entry types
tab1, tab2, tab3 = st.tabs(["Emotions", "Dreams", "Synchronicities"])

with tab1:
    st.markdown("<h3>Log Your Emotion</h3>", unsafe_allow_html=True)
    
    # Get default values or empty strings if clearing is needed
    emotion_description_default = "" if st.session_state.get('clear_emotion_form', False) else st.session_state.get('emotion_description', "")
    st.session_state.clear_emotion_form = False
    
    emotion_date = st.date_input("Date", datetime.date.today(), key="emotion_date")
    emotion_type = st.selectbox("Emotion Type", ["Joy", "Love", "Peace", "Sadness", "Fear", "Anger", "Shame", "Guilt", "Other"], key="emotion_type")
    emotion_intensity = st.slider("Intensity (1-10)", 1, 10, 5, key="emotion_intensity")
    emotion_description = st.text_area("Describe your experience", height=150, key="emotion_description", value=emotion_description_default)
    emotion_submit = st.button("Save & Generate Insight", key="emotion_submit")
    
    if emotion_submit and emotion_description:
        # Generate insight
        insight = generate_insight("emotions", emotion_description)
        
        # Create entry
        entry = {
            "type": "Emotion",
            "date": emotion_date,
            "type": emotion_type,
            "intensity": emotion_intensity,
            "description": emotion_description,
            "insight": insight
        }
        
        # Add to journal entries
        st.session_state.journal_entries.append(entry)
        
        # Display success message and insight
        st.success("Entry saved successfully!")
        st.markdown(f'<div class="insight-box"><p><strong>Insight:</strong> {insight}</p></div>', unsafe_allow_html=True)
        
        # Set flag to clear the form on next rerun
        st.session_state.clear_emotion_form = True
        st.experimental_rerun()

with tab2:
    st.markdown("<h3>Log Your Dream</h3>", unsafe_allow_html=True)
    
    # Get default values or empty strings if clearing is needed
    dream_description_default = "" if st.session_state.get('clear_dream_form', False) else st.session_state.get('dream_description', "")
    st.session_state.clear_dream_form = False
    
    dream_date = st.date_input("Date", datetime.date.today(), key="dream_date")
    dream_clarity = st.slider("Clarity (1-10)", 1, 10, 5, key="dream_clarity")
    dream_description = st.text_area("Describe your dream", height=150, key="dream_description", value=dream_description_default)
    dream_submit = st.button("Save & Generate Insight", key="dream_submit")
    
    if dream_submit and dream_description:
        # Generate insight
        insight = generate_insight("dreams", dream_description)
        
        # Create entry
        entry = {
            "type": "Dream",
            "date": dream_date,
            "clarity": dream_clarity,
            "description": dream_description,
            "insight": insight
        }
        
        # Add to journal entries
        st.session_state.journal_entries.append(entry)
        
        # Display success message and insight
        st.success("Entry saved successfully!")
        st.markdown(f'<div class="insight-box"><p><strong>Insight:</strong> {insight}</p></div>', unsafe_allow_html=True)
        
        # Set flag to clear the form on next rerun
        st.session_state.clear_dream_form = True
        st.experimental_rerun()

with tab3:
    st.markdown("<h3>Log Your Synchronicity</h3>", unsafe_allow_html=True)
    
    # Get default values or empty strings if clearing is needed
    sync_description_default = "" if st.session_state.get('clear_sync_form', False) else st.session_state.get('sync_description', "")
    st.session_state.clear_sync_form = False
    
    sync_date = st.date_input("Date", datetime.date.today(), key="sync_date")
    sync_significance = st.slider("Significance (1-10)", 1, 10, 5, key="sync_significance")
    sync_description = st.text_area("Describe your synchronicity", height=150, key="sync_description", value=sync_description_default)
    sync_submit = st.button("Save & Generate Insight", key="sync_submit")
    
    if sync_submit and sync_description:
        # Generate insight
        insight = generate_insight("synchronicities", sync_description)
        
        # Create entry
        entry = {
            "type": "Synchronicity",
            "date": sync_date,
            "significance": sync_significance,
            "description": sync_description,
            "insight": insight
        }
        
        # Add to journal entries
        st.session_state.journal_entries.append(entry)
        
        # Display success message and insight
        st.success("Entry saved successfully!")
        st.markdown(f'<div class="insight-box"><p><strong>Insight:</strong> {insight}</p></div>', unsafe_allow_html=True)
        
        # Set flag to clear the form on next rerun
        st.session_state.clear_sync_form = True
        st.experimental_rerun()

# Journal history
st.markdown("<h2>Journal History</h2>", unsafe_allow_html=True)

if not st.session_state.journal_entries:
    st.info("No journal entries yet. Start by creating a new entry above.")
else:
    # Sort entries by date (newest first)
    sorted_entries = sorted(st.session_state.journal_entries, key=lambda x: x["date"], reverse=True)
    
    # Display entries
    for i, entry in enumerate(sorted_entries):
        entry_date = entry["date"].strftime("%B %d, %Y")
        entry_type = entry["type"]
        
        # Create expandable section for each entry
        with st.expander(f"{entry_type} - {entry_date}"):
            st.markdown(f'<div class="journal-entry">', unsafe_allow_html=True)
            
            # Display entry details based on type
            if entry_type == "Emotion":
                st.markdown(f"**Intensity:** {entry['intensity']}/10", unsafe_allow_html=True)
                st.markdown(f"**Type:** {entry['type']}", unsafe_allow_html=True)
            elif entry_type == "Dream":
                st.markdown(f"**Clarity:** {entry['clarity']}/10", unsafe_allow_html=True)
            elif entry_type == "Synchronicity":
                st.markdown(f"**Significance:** {entry['significance']}/10", unsafe_allow_html=True)
            
            st.markdown(f"**Description:** {entry['description']}", unsafe_allow_html=True)
            st.markdown(f'<div class="insight-box"><p><strong>Insight:</strong> {entry["insight"]}</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Option to export journal
    if st.button("Export Journal"):
        # Convert journal entries to DataFrame
        df = pd.DataFrame(st.session_state.journal_entries)
        
        # Convert date objects to strings
        df['date'] = df['date'].apply(lambda x: x.strftime("%Y-%m-%d"))
        
        # Save to CSV
        csv_path = os.path.join(os.path.dirname(__file__), "..", "journal_export.csv")
        df.to_csv(csv_path, index=False)
        
        # Provide download link
        st.success(f"Journal exported successfully! File saved to {csv_path}")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; font-size: 0.8em;">
<p>This journal is inspired by The Law of One material from <a href="https://www.lawofone.info/" target="_blank">lawofone.info</a></p>
</div>
""", unsafe_allow_html=True)
