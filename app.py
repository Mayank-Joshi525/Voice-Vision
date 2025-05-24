import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Voice Vision | AI Language Tools",
    page_icon="🔤",
    layout="wide",
    initial_sidebar_state="collapsed"
)
from PIL import Image
import base64
import streamlit.components.v1 as components
from features.audio_app import main as audio_transcription_page
from features.trans_to import main as translation_page
from features.yt import main as youtube_analyzer_page
from features.conv import main as conversation_analysis_page 
from features.word_analogy import main as word_analogy_page 
from features.lang import main as language_learner_page
import time

# Custom CSS for Amazon-inspired UI
def local_css():
    st.markdown("""
    <style>
        /* Global Styles */
        [data-testid="stAppViewContainer"] {
            background-color: #f8f8f8;
            font-family: 'Amazon Ember', Arial, sans-serif;
        }
        
        /* Header and Navigation Bar */
        .navbar {
            background-color: #232f3e;
            padding: 8px 15px;
            display: flex;
            align-items: center;
            width: 100%;
            border-radius: 0;
            margin-bottom: 15px;
        }
        
        .nav-logo {
            color: white;
            font-size: 1.5rem;
            font-weight: 700;
            margin-right: 20px;
        }
        
        /* Navigation Buttons */
        div[data-testid="stButton"] button {
            background-color: #232f3e;
            color: #ffffff;
            border: none;
            font-size: 0.8rem;
            padding: 5px 10px;
            border-radius: 3px;
            transition: all 0.2s;
            margin: 0 2px;
            min-height: 0;
        }
        
        div[data-testid="stButton"] button:hover {
            background-color: #37475A;
        }
        
        /* Main Content */
        .container {
            padding: 0 15px;
            max-width: 1500px;
            margin: 0 auto;
        }

        /* Product Cards (Features) */
        .feature-card {
            background-color: white;
            border-radius: 4px;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            height: 100%;
            border: 1px solid #ddd;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .feature-icon {
            font-size: 1.8rem;
            margin-bottom: 10px;
            color: #232f3e;
        }
        
        .feature-title {
            font-family: 'Amazon Ember', Arial, sans-serif;
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 8px;
            color: #111;
        }
        
        .feature-description {
            font-family: 'Amazon Ember', Arial, sans-serif;
            color: #555;
            font-size: 0.85rem;
            line-height: 1.4;
        }
        
        /* Hero Section */
        .hero-section {
            background-color: white;
            padding: 20px;
            border-radius: 4px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            border: 1px solid #ddd;
        }
        
        .main-header {
            font-family: 'Amazon Ember', Arial, sans-serif;
            font-weight: 700;
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
            color: #232f3e;
        }
        
        .sub-header {
            font-family: 'Amazon Ember', Arial, sans-serif;
            font-weight: 400;
            font-size: 1.1rem;
            color: #555;
            margin-bottom: 1.5rem;
        }
        
        /* CTA Button (Amazon style) */
        .cta-button {
            background: #FFD814;
            color: #111;
            font-weight: 500;
            padding: 8px 16px;
            border-radius: 20px;
            border: none;
            cursor: pointer;
            font-size: 0.9rem;
            display: inline-block;
            text-decoration: none;
            margin-top: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .cta-button:hover {
            background: #F7CA00;
        }
        
        /* Secondary Button (Amazon style) */
        .secondary-button {
            background: #f0f2f2;
            border: 1px solid #cdcdcd;
            color: #111;
            padding: 8px 16px;
            border-radius: 3px;
            font-size: 0.9rem;
            cursor: pointer;
            margin-top: 10px;
            text-decoration: none;
            display: inline-block;
        }
        
        .secondary-button:hover {
            background: #e7e9ec;
        }
        
        /* Section Headers */
        .section-header {
            color: #111;
            font-size: 1.4rem;
            font-weight: 700;
            margin: 25px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid #ddd;
        }
        
        /* Footer Amazon Style */
        .footer {
            background-color: #232f3e;
            padding: 20px 0;
            color: #DDD;
            font-size: 0.8rem;
            text-align: center;
            margin-top: 30px;
        }
        
        .footer a {
            color: #DDD;
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        /* Carousel text animation */
        .carousel-container {
            background-color: #232f3e;
            color: white;
            padding: 8px 0;
            text-align: center;
            font-weight: 500;
            margin-bottom: 15px;
        }
        
        .carousel-text {
            display: inline-block;
            color: #FFD814;
            font-weight: bold;
            animation: fadeInOut 1.5s ease-in-out;
        }
        
        @keyframes fadeInOut {
            0% { opacity: 0; }
            20% { opacity: 1; }
            80% { opacity: 1; }
            100% { opacity: 0; }
        }
        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Responsive adjustments */
        @media only screen and (max-width: 768px) {
            .main-header {
                font-size: 1.8rem;
            }
            .sub-header {
                font-size: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)


def hero_section():
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<h1 class="main-header">Voice Vision</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Advanced AI Language Tools for Modern Communication</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-top: 15px; margin-bottom: 20px;">
            <p style="font-size: 1rem; color: #555; margin-bottom: 15px;">
            Empower your voice with Voice Vision — an innovative suite of AI-driven tools designed to revolutionize the way you interact
 with language. Whether you're transcribing conversations, translating across languages, analyzing speech patterns,
 or enhancing your language learning experience, Voice Vision delivers precision, speed, and simplicity. Built for creators, professionals,
 and learners alike, our platform brings clarity to communication in every context.</p>
            <a href="#features" class="cta-button">Explore Features</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Correct image display
        st.image("voice_vision_logo.jpg", width=400)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Amazon-style features section with functional buttons
def features_section():
    st.markdown('<div id="features"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Featured Products</h2>', unsafe_allow_html=True)
    
    # First row of features (4 columns)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎙️</div>
            <h3 class="feature-title">Audio Transcription</h3>
            <p class="feature-description">
                Convert spoken words to text with high accuracy. Perfect for meetings, interviews, and lectures.
            </p>
            <div style="margin-top: 10px;">
                <a href="/?page=audio" target="_self" class="cta-button" style="font-size: 0.8rem; padding: 5px 10px;">Try Me</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <h3 class="feature-title">Text Translation</h3>
            <p class="feature-description">
                Break language barriers with advanced translation capabilities for over 100 languages.
            </p>
            <div style="margin-top: 10px;">
                <a href="/?page=translation" target="_self" class="cta-button" style="font-size: 0.8rem; padding: 5px 10px;">Try Me</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📹</div>
            <h3 class="feature-title">YouTube Analyzer</h3>
            <p class="feature-description">
                Transcribe, summarize, and extract insights from YouTube videos without watching.
            </p>
            <div style="margin-top: 10px;">
                <a href="/?page=youtube" target="_self" class="cta-button" style="font-size: 0.8rem; padding: 5px 10px;">Try Me</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3 class="feature-title">Conversation Analysis</h3>
            <p class="feature-description">
                Get AI-powered insights from your conversations, documents, and media files.
            </p>
            <div style="margin-top: 10px;">
                <a href="/?page=conversation" target="_self" class="cta-button" style="font-size: 0.8rem; padding: 5px 10px;">Try Me</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header" style="margin-top: 30px;">More Services</h2>', unsafe_allow_html=True)
    
    # Second row of features (3 columns)
    col5, col6, col7 = st.columns(3)
    
    with col5:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔤</div>
            <h3 class="feature-title">Word Explorer</h3>
            <p class="feature-description">
               Uncover deep semantic connections between words. Perfect for research, creative writing, and educational insights — enhancing understanding through intelligent comparisons.
            </p>
            <div style="margin-top: 10px;">
                <a href="/?page=word_analogy" target="_self" class="secondary-button" style="font-size: 0.8rem; padding: 5px 10px;">Try Me</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col6:
        st.markdown("""
        <style>
            @keyframes blink {
                0% { opacity: 1; }
                50% { opacity: 0.4; }
                100% { opacity: 1; }
            }
            .new-badge {
                position: absolute; 
                top: -10px; 
                right: -10px; 
                background-color: #cc0000; 
                color: white; 
                font-size: 0.7rem; 
                font-weight: bold; 
                padding: 3px 8px; 
                border-radius: 12px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.2); 
                z-index: 1;
                animation: blink 1.5s infinite;
            }
        </style>
        <div class="feature-card">
            <div style="position: relative;">
                <div class="new-badge">NEW</div>
                <div class="feature-icon">🗣️</div>
                <h3 class="feature-title">Language Learner</h3>
                <p class="feature-description">
                  Master new languages with our interactive AI-powered learning tool. Get real-time pronunciation feedback and immersive practice — making language learning smarter, faster, and more engaging.
                </p>
                <div style="margin-top: 10px;">
                    <a href="/?page=language_learner" target="_self" class="secondary-button" style="font-size: 0.8rem; padding: 5px 10px;">Try Me</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col7:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3 class="feature-title">Vocabulary Builder</h3>
            <p class="feature-description">
                Boost your language skills with daily, AI-curated exercises. Expand your vocabulary across multiple languages through fun, effective, and personalized practice.
            </p>
            <div style="margin-top: 10px;">
                <a href="/?page=word_analogy" target="_self" class="secondary-button" style="font-size: 0.8rem; padding: 5px 10px;">Try Me</a>
            </div>
        </div>
        """, unsafe_allow_html=True)


# Footer section
def footer_section():
    st.markdown("""
    <div class="footer">
        <div style="margin-bottom: 15px;">
            <a href="https://www.linkedin.com/in/mayank-joshi5252" style="margin: 0 10px;">About Us</a>
            <a href="https://www.github.com/mayank-joshi525" style="margin: 0 10px;">Contact Us</a>
        </div>
        <p>© 2025 Voice Vision. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)


# Create carousel text component
def carousel_text():
    # Initialize session state for carousel
    if 'carousel_index' not in st.session_state:
        st.session_state.carousel_index = 0
        st.session_state.last_update = time.time()
    
    # Define carousel messages
    carousel_messages = [
        "See The Difference!",
        "Simplify Your Workflow!",
        "Bridge Communication Gaps!",
        "Enjoy Peace Of Mind!",
        "Secure your edge!"
    ]
    
    # Update carousel index every 3 seconds
    current_time = time.time()
    if current_time - st.session_state.last_update > 3:
        st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(carousel_messages)
        st.session_state.last_update = current_time
    
    # Display carousel text
    st.markdown(f"""
    <div class="carousel-container">
        <span>Voice Vision- </span>
        <span class="carousel-text">{carousel_messages[st.session_state.carousel_index]}</span>
    </div>
    """, unsafe_allow_html=True)


# Main app with Amazon-style UI
def main():
    local_css()
    
    # Initialize session state for page navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # Check for URL parameter for page navigation
    # Replaced st.experimental_get_query_params with st.query_params
    if "page" in st.query_params:
        st.session_state.current_page = st.query_params["page"]
    
    # Amazon-style navigation bar
    st.markdown("""
    <div class="navbar">
        <span class="nav-logo">Voice Vision</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Smaller navigation buttons
    cols = st.columns(7)
    with cols[0]:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.query_params.page = 'home'
            st.rerun()
    with cols[1]:
        if st.button("Transcriptor", use_container_width=True):
            st.session_state.current_page = 'audio'
            st.query_params.page = 'audio'
            st.rerun()
    with cols[2]:
        if st.button("Translator", use_container_width=True):
            st.session_state.current_page = 'translation'
            st.query_params.page = 'translation'
            st.rerun()
    with cols[3]:
        if st.button("YouTube Analyzer", use_container_width=True):
            st.session_state.current_page = 'youtube'
            st.query_params.page = 'youtube'
            st.rerun()
    with cols[4]:
        if st.button("Conversation Analyzer", use_container_width=True):
            st.session_state.current_page = 'conversation'
            st.query_params.page = 'conversation'
            st.rerun()
    with cols[5]:
        if st.button("Word Explorer", use_container_width=True):
            st.session_state.current_page = 'word_analogy'
            st.query_params.page = 'word_analogy'
            st.rerun()
    with cols[6]:
        if st.button("Language Learner", use_container_width=True):
            st.session_state.current_page = 'language_learner'
            st.query_params.page = 'language_learner'
            st.rerun()
    
    # Add carousel text below navigation
    carousel_text()
    
    # Content container
    st.markdown('<div class="container">', unsafe_allow_html=True)
    
    # Display the appropriate page based on navigation
    if st.session_state.current_page == 'audio':
        audio_transcription_page()
    elif st.session_state.current_page == 'translation':
        translation_page()
    elif st.session_state.current_page == 'youtube':
        youtube_analyzer_page()
    elif st.session_state.current_page == 'conversation':
        conversation_analysis_page()
    elif st.session_state.current_page == 'word_analogy':
        word_analogy_page()
    elif st.session_state.current_page == 'language_learner': 
        language_learner_page()
    else:
        hero_section()
        features_section()
    
    st.markdown('</div>', unsafe_allow_html=True)
    footer_section()

if __name__ == "__main__":
    main()