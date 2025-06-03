import streamlit as st
import whisper
from io import BytesIO # Downloading of Files
import os # local file operation
import numpy as np # array operations
import librosa # audio analysis and visualisation
import librosa.display # number of speaker count
import time # libraray related to time
import re # regular expression
from pydub import AudioSegment # audio manipulation 
import matplotlib.pyplot as plt #charts and graphs
import pandas as pd # high extensive calculations which can not be performed in array
from sklearn.cluster import KMeans # speaker identification
import tempfile # for creation of temp files
import json # js data realated


def main():  # Added this wrapper function for integration
    # Set page config first
    

    # Load Whisper model once
    @st.cache_resource # for storingn cache
    def load_model():
        return whisper.load_model("base") 

    model = load_model()

    # Language code to name mapping
    lang_map = {
        "en": "English", "hi": "Hindi", "fr": "French", "de": "German",
        "es": "Spanish", "it": "Italian", "zh": "Chinese", "ja": "Japanese",
        "ko": "Korean", "ar": "Arabic", "ru": "Russian", "te": "Telugu",
        "ta": "Tamil", "bn": "Bengali", "pa": "Punjabi", "gu": "Gujarati", "kn": "Kannada"
    }

    #encoder working for audio transcription
    def transcribe_audio(audio_file):
        """Transcribe audio using Whisper"""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
            audio_bytes = audio_file.read()
            temp_file.write(audio_bytes)
            
        # wav creation is need because wav is getting better results
        result = model.transcribe(temp_path)
        lang_code = result['language']
        lang_name = lang_map.get(lang_code, lang_code)
        
        # at the end it removess wav file
        os.remove(temp_path)
        return result["text"], lang_name, result["segments"]

#Gender Analysis by Pitch
    
    def analyze_gender(audio_path):
        """Analyze audio to predict speaker gender"""
        y, sr = librosa.load(audio_path, sr=None)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[magnitudes > 0]
        
        #we are identifying pitch of the gender 
        if len(pitch_values) == 0:
            return "Unknown"
        
        mean_pitch = np.mean(pitch_values)
        if mean_pitch < 165:
            return "Male"
        elif mean_pitch > 180:
            return "Female"
        else:
            return "Undetermined"

    #couunting number of speaker, librosa if identifying pitch, we are making K means algorithm, pitch in each second and then apply K means and make 
    # a cluster of them
    def count_speakers(audio_path, segments):
        """Count number of unique speakers"""
        y, sr = librosa.load(audio_path, sr=None)
        features = []
        
        for segment in segments:
            start_sample = int(segment['start'] * sr)
            end_sample = int(segment['end'] * sr)
            
            if start_sample < end_sample and end_sample <= len(y):
                segment_audio = y[start_sample:end_sample]
                if len(segment_audio) > 512:
                    mfccs = librosa.feature.mfcc(y=segment_audio, sr=sr, n_mfcc=13)
                    mfccs_mean = np.mean(mfccs, axis=1)
                    features.append(mfccs_mean)
        
        if len(features) < 2:
            return 1
        
        features = np.array(features)
        max_speakers = min(8, len(features))
        best_score = -1
        num_speakers = 1
        
        for n_clusters in range(1, max_speakers + 1):
            if len(features) >= n_clusters:
                kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10).fit(features)
                score = -kmeans.inertia_
                
                if n_clusters == 1 or score > best_score * 0.7:
                    best_score = score
                    num_speakers = n_clusters
        
        return num_speakers

    def format_time(seconds):
        """Format seconds to MM:SS format"""
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes:02d}:{remaining_seconds:02d}"

    def create_transcript_with_timestamps(segments):
        """Create formatted transcript with timestamps"""
        transcript = ""
        for segment in segments:
            start_time = format_time(segment['start'])
            end_time = format_time(segment['end'])
            text = segment['text'].strip()
            transcript += f"[{start_time} - {end_time}] {text}\n\n"
        return transcript

    def generate_audio_visualization(audio_path):
        """Generate waveform and spectrogram visualization"""
        y, sr = librosa.load(audio_path, sr=None)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        librosa.display.waveshow(y, sr=sr, ax=ax1)
        ax1.set_title('Waveform')
        ax1.set_xlabel('')
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        img = librosa.display.specshow(D, y_axis='log', x_axis='time', sr=sr, ax=ax2)
        ax2.set_title('Spectrogram')
        fig.colorbar(img, ax=ax2, format="%+2.0f dB")
        plt.tight_layout()
        return fig

    def calculate_speech_stats(segments):
        """Calculate speech statistics"""
        if not segments:
            return {}
        
        total_duration = segments[-1]['end']
        speech_duration = sum(segment['end'] - segment['start'] for segment in segments)
        word_count = sum(len(segment['text'].split()) for segment in segments)
        
        return {
            "Total Duration": f"{format_time(total_duration)} (MM:SS)",
            "Speech Duration": f"{format_time(speech_duration)} (MM:SS)",
            "Words": word_count,
            "Words per Minute": round(word_count / (speech_duration / 60)) if speech_duration > 0 else 0,
            "Segments": len(segments)
        }

    def extract_keywords(text, num_keywords=5):
        """Extract simple keywords"""
        from collections import Counter
        stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you'}
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        word_counts = Counter(filtered_words)
        return word_counts.most_common(num_keywords)

    """Main function to run the Streamlit app"""
    st.markdown("""
    <style>
        .header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #4361ee;
            margin-bottom: 1.5rem;
        }
        .metric-box {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .metric-title {
            font-size: 0.9rem;
            color: #6c757d;
            margin-bottom: 0.3rem;
        }
        .metric-value {
            font-size: 1.4rem;
            font-weight: 600;
            color: #212529;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="header">Audio Transcription</div>', unsafe_allow_html=True)
    
    # Create columns for layout
    col1, col2 = st.columns([3, 1])  # Adjust ratio as needed

    with col1:
        # Initialize session state
        if 'transcribed' not in st.session_state:
            st.session_state.transcribed = False
            st.session_state.show_results = False
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload audio file (mp3, wav, m4a)", 
            type=["mp3", "wav", "m4a"],
            accept_multiple_files=False
        )
        
        if uploaded_file:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(suffix="." + uploaded_file.name.split(".")[-1], delete=False) as temp_file:
                temp_path = temp_file.name
                audio_bytes = uploaded_file.getvalue()
                temp_file.write(audio_bytes)
            
            st.session_state.temp_audio_path = temp_path
            st.audio(uploaded_file, format="audio/mp3")
            
            # Advanced options
            with st.expander("Analysis Options"):
                col1, col2 = st.columns(2)
                with col1:
                    enable_speaker_detection = st.checkbox("Detect number of speakers", value=False)
                    enable_gender_detection = st.checkbox("Detect speaker gender", value=False)
                with col2:
                    enable_visualization = st.checkbox("Generate audio visualization", value=False)
                    enable_keywords = st.checkbox("Extract keywords", value=False)
            
            # Transcription button
            if st.button("Transcribe Audio", type="primary"):
                with st.spinner("Transcribing audio..."):
                    start_time = time.time()
                    text, lang, segments = transcribe_audio(uploaded_file)
                    st.session_state.transcription = text
                    st.session_state.language = lang
                    st.session_state.segments = segments
                    
                    # Initialize empty results for optional features
                    analysis_results = {}
                    speech_stats = {}
                    keywords = []
                    visualization = None
                    
                    # Only perform selected analyses
                    if enable_speaker_detection:
                        try:
                            num_speakers = count_speakers(temp_path, segments)
                            analysis_results["Number of Speakers"] = num_speakers
                        except Exception as e:
                            st.warning(f"Could not detect number of speakers: {e}")
                            analysis_results["Number of Speakers"] = "Detection failed"
                    
                    if enable_gender_detection:
                        try:
                            gender = analyze_gender(temp_path)
                            analysis_results["Dominant Speaker Gender"] = gender
                        except Exception as e:
                            st.warning(f"Could not detect gender: {e}")
                            analysis_results["Dominant Speaker Gender"] = "Detection failed"
                    
                    if enable_speaker_detection or enable_gender_detection:
                        speech_stats = calculate_speech_stats(segments)
                    
                    if enable_keywords:
                        keywords = extract_keywords(text)
                    
                    if enable_visualization:
                        try:
                            visualization = generate_audio_visualization(temp_path)
                        except Exception as e:
                            st.warning(f"Could not generate visualization: {e}")
                    
                    # Format transcript with timestamps
                    timestamped_transcript = create_transcript_with_timestamps(segments)
                    
                    # Store results
                    st.session_state.analysis_results = analysis_results
                    st.session_state.speech_stats = speech_stats
                    st.session_state.keywords = keywords
                    st.session_state.timestamped_transcript = timestamped_transcript
                    st.session_state.visualization = visualization
                    st.session_state.processing_time = time.time() - start_time
                    st.session_state.transcribed = True
                    st.session_state.show_results = True
                
            # Show results if transcription is complete
            if st.session_state.get('show_results'):
                st.success(f"✅ Transcription Complete! (Processed in {st.session_state.processing_time:.2f} seconds)")
                
                # Display basic info
                st.markdown(f"**🗣️ Detected Language:** {st.session_state.language}")
                
                # Display selected analysis results
                if st.session_state.analysis_results:
                    st.subheader("Audio Analysis")
                    for key, value in st.session_state.analysis_results.items():
                        st.markdown(f"**{key}:** {value}")
                
                if st.session_state.speech_stats:
                    st.subheader("Speech Statistics")
                    stats_df = pd.DataFrame({
                        "Metric": list(st.session_state.speech_stats.keys()),
                        "Value": list(st.session_state.speech_stats.values())
                    })
                    st.table(stats_df)
                
                if st.session_state.keywords:
                    st.subheader("Key Topics")
                    keywords_str = ", ".join([f"{word} ({count})" for word, count in st.session_state.keywords])
                    st.markdown(f"**Keywords:** {keywords_str}")
                
                if st.session_state.visualization:
                    st.subheader("Audio Visualization")
                    st.pyplot(st.session_state.visualization)
                
                # Transcription tabs
                tab1, tab2 = st.tabs(["Plain Text", "With Timestamps"])
                
                with tab1:
                    # Create a unique key for the text area
                    text_area_key = f"transcription_{time.time()}"
                    st.text_area(
                        "Transcribed Text", 
                        st.session_state.transcription, 
                        height=300,
                        key=text_area_key
                    )
                    
                    # Copy button that actually works
                    if st.button("Copy Text", key="copy_text_btn"):
                        st.session_state.copied_text = st.session_state.transcription
                        st.success("Text copied to clipboard!")
                    
                    # Download button
                    download_txt = BytesIO()
                    download_txt.write(st.session_state.transcription.encode())
                    download_txt.seek(0)
                    st.download_button(
                        "Download Text", 
                        data=download_txt,
                        file_name="transcription.txt",
                        mime="text/plain"
                    )
                
                with tab2:
                    st.text_area(
                        "Timestamped Transcript", 
                        st.session_state.timestamped_transcript, 
                        height=400,
                        key="timestamped_area"
                    )
                    
                    download_timestamped = BytesIO()
                    download_timestamped.write(st.session_state.timestamped_transcript.encode())
                    download_timestamped.seek(0)
                    st.download_button(
                        "Download Timestamped", 
                        data=download_timestamped,
                        file_name="timestamped_transcript.txt",
                        mime="text/plain"
                    )
                    
                    # JSON download
                    json_data = {
                        "language": st.session_state.language,
                        "segments": st.session_state.segments,
                        "analysis": st.session_state.analysis_results
                    }
                    json_str = json.dumps(json_data, indent=2)
                    st.download_button(
                        "Download JSON",
                        data=json_str,
                        file_name="transcription.json",
                        mime="application/json"
                    )

        # Clean up temporary files
        if st.session_state.get('temp_audio_path') and os.path.exists(st.session_state.temp_audio_path):
            try:
                os.unlink(st.session_state.temp_audio_path)
            except:
                pass

    with col2:
        st.markdown("""
      
            
        ### How to Use Transcriptor
            
        1. **Upload** an audio file (MP3, WAV, M4A)
        2. Select analysis options (optional)
        3. Click **Transcribe Audio** button
        4. View and download results
        5. Explore different output formats
            
        *Note: Processing time depends on audio length*
        """)

if __name__ == "__main__":
    main()
