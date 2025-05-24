import streamlit as st
import requests
from gtts import gTTS
import base64
import os
from pathlib import Path

def main():
    
# --- Audio Functions ---
    def text_to_speech(text, lang='en'):
        """Convert text to speech and return audio file"""
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            audio_file = Path(f"temp_audio_{hash(text)}.mp3")  # Unique filename
            tts.save(audio_file)
            return audio_file
        except Exception as e:
            st.error(f"Error generating speech: {str(e)}")
            return None
    
    def show_audio_player(file_path):
        """Show audio player with play button"""
        try:
            with open(file_path, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                md = f"""
                    <audio controls>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    Your browser does not support the audio element.
                    </audio>
                    """
                st.markdown(md, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error creating audio player: {str(e)}")
    
    def cleanup_audio_files():
        """Remove any temporary audio files"""
        try:
            for file in Path(".").glob("temp_audio_*.mp3"):
                try:
                    file.unlink()
                except:
                    pass
        except:
            pass
    
    # --- Word Data Functions ---
    def get_synonyms(word):
        """Get synonyms from Datamuse API"""
        try:
            response = requests.get(f"https://api.datamuse.com/words?rel_syn={word}", timeout=5)
            if response.status_code == 200:
                return [item['word'] for item in response.json()[:5]]
            return []
        except Exception as e:
            st.error(f"Error fetching synonyms: {str(e)}")
            return []
    
    def get_antonyms(word):
        """Get antonyms from Datamuse API"""
        try:
            response = requests.get(f"https://api.datamuse.com/words?rel_ant={word}", timeout=5)
            if response.status_code == 200:
                return [item['word'] for item in response.json()[:5]]
            return []
        except Exception as e:
            st.error(f"Error fetching antonyms: {str(e)}")
            return []
    
    def get_examples(word):
        """Get better example sentences"""
        try:
            examples = [
                f"I felt {word} when I received the good news yesterday.",
                f"Her {word} smile brightened up the entire room.",
                f"The children were absolutely {word} to see their grandparents after so long.",
                f"We should try to remain {word} even during difficult times.",
                f"His inherently {word} personality makes him popular among his colleagues."
            ]
            return examples[:3]
        except Exception as e:
            st.error(f"Error generating examples: {str(e)}")
            return []
    
    # --- Streamlit UI ---
    st.title("📚 Smart Word Explorer")
    st.markdown("Discover Synonyms, Antonyms and Usage Examples")
    
    # Initialize session state
    if 'audio_file' not in st.session_state:
        st.session_state.audio_file = None
    
    word = st.text_input("Enter any English word", value="", key="word_input", 
                        placeholder="Type a word and click Analyze").strip().lower()
    
    if st.button("Analyze Word"):
        cleanup_audio_files()  # Clean up previous audio files
        
        if word:
            with st.spinner(f"Analyzing '{word}'..."):
                # Generate audio file
                st.session_state.audio_file = text_to_speech(word)
                
                # Get word data
                synonyms = get_synonyms(word)
                antonyms = get_antonyms(word)
                examples = get_examples(word)
                
                # Display results
                st.subheader(f"Word: {word.capitalize()}")
                
                # Show audio player if audio was generated
                if st.session_state.audio_file:
                    st.markdown("**Pronunciation**")
                    show_audio_player(st.session_state.audio_file)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Synonyms**")
                    if synonyms:
                        st.write(", ".join([s.capitalize() for s in synonyms]))
                    else:
                        st.write("No synonyms found")
                
                with col2:
                    st.markdown("**Antonyms**")
                    if antonyms:
                        st.write(", ".join([a.capitalize() for a in antonyms]))
                    else:
                        st.write("No antonyms found")
                
                st.markdown("**Example Sentences**")
                if examples:
                    for example in examples:
                        st.write(f"- {example.capitalize()}")
                else:
                    st.write("No examples found")
        else:
            st.warning("Please enter a word")
    
    # Clean up when done
    cleanup_audio_files()
    
    st.markdown("---")
    
    # Add some space at the bottom
    st.markdown("<br><br>", unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()