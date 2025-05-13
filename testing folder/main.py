import streamlit as st
from PIL import Image
import base64
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Voice Vision | AI Language Tools",
    page_icon="🔤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
def local_css():
    st.markdown("""
    <style>
        /* Main styling */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4edf8 100%);
        }
        
        .main-header {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
            font-size: 3.2rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #3a7bd5, #00d2ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }
        
        .sub-header {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 400;
            font-size: 1.5rem;
            color: #555;
            margin-bottom: 2rem;
        }
        
        .feature-card {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            height: 100%;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.12);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(90deg, #3a7bd5, #00d2ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .feature-title {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 600;
            font-size: 1.3rem;
            margin-bottom: 0.5rem;
            color: #333;
        }
        
        .feature-description {
            font-family: 'Helvetica Neue', sans-serif;
            color: #666;
            font-size: 1rem;
        }
        
        .cta-button {
            background: linear-gradient(90deg, #3a7bd5, #00d2ff);
            color: white;
            font-weight: 600;
            padding: 0.8rem 2rem;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            font-size: 1.1rem;
            transition: transform 0.3s, box-shadow 0.3s;
            display: inline-block;
            text-decoration: none;
            margin-top: 1rem;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .footer {
            text-align: center;
            padding: 2rem 0;
            color: #777;
            font-size: 0.9rem;
        }
        
        /* Custom section styles */
        .hero-section {
            padding: 3rem 0;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .features-section {
            padding: 2rem 0;
        }
        
        .testimonials-section {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9f1f7 100%);
            padding: 3rem 0;
            margin: 3rem 0;
            border-radius: 10px;
        }
        
        .contact-section {
            padding: 3rem 0;
            text-align: center;
        }
        
        /* Stats section */
        .stats-container {
            display: flex;
            justify-content: space-around;
            margin: 2rem 0;
            text-align: center;
        }
        
        .stat-item {
            padding: 1rem;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #3a7bd5, #00d2ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label {
            font-size: 1rem;
            color: #555;
        }
        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Responsive adjustments */
        @media only screen and (max-width: 768px) {
            .main-header {
                font-size: 2.5rem;
            }
            .sub-header {
                font-size: 1.2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Hero section
def hero_section():
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">Voice Vision</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Advanced AI Language Tools for Modern Communication</p>', unsafe_allow_html=True)
    
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="padding: 2rem;">
            <h2 style="font-size: 1.8rem; margin-bottom: 1.5rem; color: #333;">Transforming how you work with language</h2>
            <p style="font-size: 1.1rem; color: #555; margin-bottom: 1.5rem; text-align: left;">
                Our suite of AI-powered tools helps you transcribe, translate, analyze, and learn languages with unprecedented accuracy and efficiency.
            </p>
            <div style="text-align: left;">
                <a href="#features" class="cta-button">Explore Features</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Hero image
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <img src="https://images.unsplash.com/photo-1589254065878-42c9da997008?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80" 
                 style="max-width: 100%; height: auto; border-radius: 10px; box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);">
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Features section
def features_section():
    st.markdown('<div class="features-section" id="features">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; margin-bottom: 3rem; color: #333; font-size: 2rem;">Our Powerful Features</h2>', unsafe_allow_html=True)
    
    # First row of features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎙️</div>
            <h3 class="feature-title">Audio Transcription</h3>
            <p class="feature-description">
                Convert spoken words to text with our high-accuracy AI transcription tool. Perfect for meetings, interviews, and lectures.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <h3 class="feature-title">Text Translation</h3>
            <p class="feature-description">
                Break language barriers with our advanced neural translation engine supporting over 100 languages with contextual understanding.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📹</div>
            <h3 class="feature-title">YouTube Video Analyzer</h3>
            <p class="feature-description">
                Automatically transcribe and summarize YouTube videos to extract key insights without watching the entire content.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row of features
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🗣️</div>
            <h3 class="feature-title">Language Learner</h3>
            <p class="feature-description">
                Accelerate your language learning with personalized exercises, pronunciation feedback, and interactive conversations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col5:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <h3 class="feature-title">Conversation Analysis</h3>
            <p class="feature-description">
                Upload text, PDFs, or audio files and get detailed analysis, insights, and answers to your specific questions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col6:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3 class="feature-title">Word Analogy</h3>
            <p class="feature-description">
                Discover synonyms, antonyms, and usage examples to enhance your vocabulary and improve your writing.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Spacer section
def spacer_section():
    st.markdown("""
    <div style="margin: 4rem 0;">
    </div>
    """, unsafe_allow_html=True)

# Vision section
def vision_section():
    st.markdown('<div class="vision-section" style="padding: 3rem 0;">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; margin-bottom: 2rem; color: #333; font-size: 2rem;">Our Vision</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; max-width: 800px; margin: 0 auto;">
        <p style="color: #555; font-size: 1.1rem; line-height: 1.6;">
            At Voice Vision, we believe that language should never be a barrier to understanding and connection. 
            Our mission is to build AI-powered tools that transform how people interact with spoken and written content,
            making communication seamless across languages, formats, and platforms.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Call to action section
def cta_section():
    st.markdown("""
    <div class="contact-section">
        <h2 style="text-align: center; margin-bottom: 1.5rem; color: #333; font-size: 2rem;">Ready to Transform Your Language Experience?</h2>
        <p style="text-align: center; margin-bottom: 2rem; color: #555; font-size: 1.1rem;">
            Experience the future of language technology with Voice Vision.
        </p>
        <div style="text-align: center;">
            <a href="#" class="cta-button" style="font-size: 1.2rem; padding: 1rem 2.5rem;">Get Started Now</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer section
def footer_section():
    st.markdown("""
    <div class="footer">
                    <p>© 2025 Voice Vision. All rights reserved.</p>
        <p>Contact: info@voicevision.ai | Support: support@voicevision.ai</p>
    </div>
    """, unsafe_allow_html=True)

# Main app
def main():
    local_css()
    hero_section()
    features_section()
    spacer_section()
    vision_section()
    cta_section()
    footer_section()

if __name__ == "__main__":
    main()