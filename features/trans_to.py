import streamlit as st
import time
import os
import tempfile
from googletrans import Translator
from io import BytesIO
import speech_recognition as sr
from gtts import gTTS

def main():
    # Apply your app's styling with white background
    st.markdown("""
    <style>
        /* Main styling with white background */
        [data-testid="stAppViewContainer"] {
            background-color: white;
        }
        .header {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            color: #3a7bd5;
            display: inline-block;
        }
        .feature-card {
            padding: 15px;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            border: 1px solid #e0e0e0;
        }
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        /* How to use section styling */
        .how-to-use {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="header">🌐 Voice Vision Translator</h1>', unsafe_allow_html=True)
    st.markdown("Translate Text and Voice between multiple languages with ease")

    # Add "How to Use" section
    with st.expander("📌 How to Use This Translator", expanded=False):
        st.markdown("""
        **1. Text Translation:**
        - Select source and target languages
        - Type or paste your text
        - Click 'Translate Text' button
        
        **2. Voice Translation:**
        - Select your speaking language
        - Click 'Start' to begin recording
        - Speak clearly into your microphone
        - Click 'Stop' when finished
        - Select target language and click 'Translate Voice Input'
        
        **3. History:**
        - View all your past translations
        - Play audio of translations
        - Clear history when needed
        """)

    # Initialize translator
    translator = Translator()

    # Language code to name mapping
    lang_map = {
        "en": "English", "hi": "Hindi", "fr": "French", "de": "German",
        "es": "Spanish", "it": "Italian", "zh-cn": "Chinese", "ja": "Japanese",
        "ko": "Korean", "ar": "Arabic", "ru": "Russian", "te": "Telugu",
        "ta": "Tamil", "bn": "Bengali", "pa": "Punjabi", "gu": "Gujarati", "kn": "Kannada"
    }
    lang_codes = {v: k for k, v in lang_map.items()}

    # Initialize session state for history
    if 'translation_history' not in st.session_state:
        st.session_state.translation_history = []

    # Initialize session states for audio playback
    if 'should_play_audio' not in st.session_state:
        st.session_state.should_play_audio = False
    if 'audio_text' not in st.session_state:
        st.session_state.audio_text = ""
    if 'audio_lang' not in st.session_state:
        st.session_state.audio_lang = "en"

    # Initialize session states for recording control
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    if 'recording_complete' not in st.session_state:
        st.session_state.recording_complete = False
    if 'voice_text' not in st.session_state:
        st.session_state.voice_text = ""
    if 'manual_stop' not in st.session_state:
        st.session_state.manual_stop = False
    if 'recording_data' not in st.session_state:
        st.session_state.recording_data = None

    # Function to add entry to translation history
    def add_to_history(source_text, source_lang, translated_text, target_lang):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.translation_history.append({
            "timestamp": timestamp,
            "source_language": source_lang,
            "source_text": source_text,
            "target_language": target_lang,
            "translated_text": translated_text
        })

    # Function to create a download link for text
    def get_text_download_link(text, filename="translation.txt"):
        b = BytesIO()
        b.write(text.encode())
        b.seek(0)
        return st.download_button("📥 Download Translation", b, file_name=filename)

    # Function to play audio without affecting translated text display
    def play_audio(text, lang_code):
        try:
            if not text:
                st.warning("No text available to play")
                return None
                
            tts = gTTS(text=text, lang=lang_code)
            
            # Use a consistent path to avoid regenerating files when not needed
            audio_path = os.path.join(tempfile.gettempdir(), f"voice_vision_audio_{lang_code}.mp3")
            tts.save(audio_path)
            
            # Return the audio bytes
            with open(audio_path, "rb") as audio_file:
                return audio_file.read()
                
        except Exception as e:
            st.error(f"Error generating audio: {e}")
            return None

    # Create tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["💬 Text Input", "🎤 Microphone Input", "📚 History"])

    with tab1:
        st.header("Text Translation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Source")
            source_lang = st.selectbox("Select source language", list(lang_map.values()), index=0, key="text_source_lang")
            input_text = st.text_area("Enter text to translate", height=150)
        
        with col2:
            st.subheader("Translation")
            target_lang = st.selectbox("Select target language", list(lang_map.values()), index=1, key="text_target_lang")
            
            # Quick language swap button
            if st.button("🔄 Swap Languages", key="text_swap"):
                source_lang, target_lang = target_lang, source_lang
                st.experimental_rerun()
                
            translation_container = st.container()
            
            if st.button("🌐 Translate Text", key="text_translate", use_container_width=True) and input_text:
                try:
                    with st.spinner("Translating..."):
                        result = translator.translate(
                            input_text, 
                            src=lang_codes[source_lang], 
                            dest=lang_codes[target_lang]
                        )
                        translated_text = result.text
                        
                        # Display translated text
                        with translation_container:
                            st.success("✅ Translation Complete!")
                            st.session_state.last_translated_text = translated_text
                            st.session_state.last_translated_lang = lang_codes[target_lang]
                            st.text_area("Translated Text", translated_text, height=150, key="text_translation_result")
                            
                            # Provide download option
                            get_text_download_link(translated_text, f"translation_{target_lang}.txt")
                            
                            # Add text-to-speech option
                            audio_bytes = play_audio(translated_text, lang_codes[target_lang])
                            if audio_bytes:
                                st.audio(audio_bytes, format="audio/mp3")
                        
                        # Add to translation history
                        add_to_history(input_text, source_lang, translated_text, target_lang)
                
                except Exception as e:
                    st.error(f"Translation Error: {e}")

    with tab2:
     
        
        # Functions to control recording state
        def start_recording_session():
            st.session_state.is_recording = True
            st.session_state.recording_complete = False
            st.session_state.manual_stop = False
            
        def stop_recording_session():
            st.session_state.is_recording = False
            st.session_state.recording_complete = True
            st.session_state.manual_stop = True
        
        def pause_recording_session():
            st.session_state.is_recording = False
        
        def resume_recording_session():
            st.session_state.is_recording = True
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Voice Input")
            mic_source_lang = st.selectbox("Select your speaking language", list(lang_map.values()), index=0, key="mic_source_lang")
            
            # Voice recording control buttons
            col_rec1, col_rec2, col_rec3 = st.columns(3)
            with col_rec1:
                start_button = st.button("🎤 Start", key="start_recording", 
                                        on_click=start_recording_session, 
                                        disabled=st.session_state.is_recording)
            with col_rec2:
                pause_button = st.button("⏸️ Pause", key="pause_recording", 
                                       on_click=pause_recording_session,
                                       disabled=not st.session_state.is_recording)
            with col_rec3:
                stop_button = st.button("⏹️ Stop", key="stop_recording", 
                                       on_click=stop_recording_session,
                                       disabled=not st.session_state.is_recording and not st.session_state.recording_complete)
            
            # Recording status indicator
            recording_status = st.empty()
            if st.session_state.is_recording:
                recording_status.markdown("#### 🔴 Recording in progress...")
                recording_status.markdown("Speak clearly and press 'Stop' when finished.")
            elif hasattr(st.session_state, 'recording_paused') and st.session_state.recording_paused:
                recording_status.markdown("#### ⏸️ Recording paused")
                recording_status.markdown("Press 'Resume' to continue or 'Stop' to finish.")
            
            # Simplified recording settings
            st.markdown("### Recording Settings")
            auto_complete = st.checkbox("Enable auto-completion", value=False,
                                       help="When enabled, recording will stop after detecting silence")
            
            if auto_complete:
                recording_timeout = st.slider("Silence Timeout (seconds)", min_value=2, max_value=30, value=5, 
                                            help="Time of silence before auto-stopping")
            else:
                recording_timeout = 30
            
            # Placeholder for transcribed text
            transcribed_text = st.empty()
        
        with col2:
            st.subheader("Translation")
            mic_target_lang = st.selectbox("Translate to", list(lang_map.values()), index=1, key="mic_target_lang")
            
            # Container for translation output
            voice_translation_container = st.container()
            
            translate_button = st.button("🌐 Translate Voice Input", key="translate_voice", 
                                       disabled=not st.session_state.recording_complete,
                                       use_container_width=True)
        
        # Handle active recording    
        if st.session_state.is_recording:
            # Initialize recognizer
            r = sr.Recognizer()
            
            try:
                with st.spinner("Listening... Speak now"):
                    # Use microphone as source
                    with sr.Microphone() as source:
                        r.energy_threshold = 1000
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        r.pause_threshold = 0.8
                        
                        if not auto_complete:
                            recording_timeout = 60
                            
                        audio = r.listen(source, timeout=recording_timeout if auto_complete else None, 
                                       phrase_time_limit=recording_timeout * 2)
                        
                        st.session_state.recording_data = audio
                        
                st.success("Audio captured! Click 'Translate Voice Input' to process.")
                st.session_state.recording_complete = True
                st.session_state.is_recording = False
                    
            except sr.UnknownValueError:
                st.error("Could not understand audio")
                st.session_state.is_recording = False
            except sr.RequestError as e:
                st.error(f"Could not request results from Google Speech Recognition service; {e}")
                st.session_state.is_recording = False
            except Exception as e:
                st.error(f"Error recording: {e}")
                st.session_state.is_recording = False
        
        # Handle translation when button is clicked
        if translate_button and st.session_state.recording_complete and hasattr(st.session_state, 'recording_data'):
            try:
                r = sr.Recognizer()
                
                with st.spinner("Processing speech..."):
                    voice_text = r.recognize_google(st.session_state.recording_data, 
                                                  language=lang_codes[mic_source_lang])
                    
                    st.session_state.voice_text = voice_text
                    
                    transcribed_text.text_area("Transcribed Text", voice_text, height=100)
                    
                    # Translate the transcribed text
                    with st.spinner("Translating..."):
                        result = translator.translate(
                            voice_text,
                            src=lang_codes[mic_source_lang],
                            dest=lang_codes[mic_target_lang]
                        )
                        voice_translated_text = result.text
                        
                        st.session_state.voice_translated_text = voice_translated_text
                        st.session_state.voice_translated_lang = lang_codes[mic_target_lang]
                        
                        with voice_translation_container:
                            st.text_area("Translation", voice_translated_text, height=100, key="voice_translation_result")
                            
                            add_to_history(voice_text, mic_source_lang, voice_translated_text, mic_target_lang)
                            
                            audio_bytes = play_audio(voice_translated_text, lang_codes[mic_target_lang])
                            if audio_bytes:
                                st.audio(audio_bytes, format="audio/mp3")
                    
            except sr.UnknownValueError:
                st.error("Could not understand audio. Please try recording again.")
            except sr.RequestError as e:
                st.error(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                st.error(f"Error: {e}")

    with tab3:
        st.header("Translation History")
        
        if len(st.session_state.translation_history) > 0:
            history = sorted(
                st.session_state.translation_history, 
                key=lambda x: x.get("timestamp", ""), 
                reverse=True
            )
            
            for i, entry in enumerate(history):
                timestamp = entry.get("timestamp", "Unknown time")
                with st.expander(f"{entry['source_language']} → {entry['target_language']} ({timestamp})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Source ({entry['source_language']}):**")
                        st.text_area(f"Source Text {i}", entry['source_text'], height=100, key=f"src_{i}")
                    
                    with col2:
                        st.markdown(f"**Translation ({entry['target_language']}):**")
                        st.text_area(f"Translated Text {i}", entry['translated_text'], height=100, key=f"trs_{i}")
                    
                    if st.button(f"🔊 Play Translation", key=f"play_{i}"):
                        audio_bytes = play_audio(entry['translated_text'], lang_codes[entry['target_language']])
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")
            
            if st.button("🗑️ Clear History"):
                st.session_state.translation_history = []
                st.experimental_rerun()
                
        else:
            st.info("No translation history yet. Start translating to build your history!")

if __name__ == "__main__":
    main()