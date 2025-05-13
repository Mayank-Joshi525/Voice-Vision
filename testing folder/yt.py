import streamlit as st
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import os
import re
from gtts import gTTS
import tempfile
import nltk
from collections import Counter

# Download nltk data (first time only)
nltk.download('punkt')

# YouTube API setup
YOUTUBE_API_KEY = 'AIzaSyCXN-YPhoilxFUiSkKag7qHxFhvrVh7EoA'  # Replace with your actual API key

def get_video_id(url):
    """Extracts video ID from YouTube URL"""
    video_id = url.split('v=')[-1]
    if '&' in video_id:
        video_id = video_id.split('&')[0]
    return video_id

def get_video_details(video_id):
    """Fetch video details (title, thumbnail, duration) from YouTube API"""
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.videos().list(part="snippet,contentDetails", id=video_id)
    response = request.execute()
    
    if 'items' in response:
        video_details = response['items'][0]['snippet']
        content_details = response['items'][0]['contentDetails']
        title = video_details['title']
        thumbnail_url = video_details['thumbnails']['high']['url']
        
        # Parse duration (ISO 8601 format)
        duration = content_details['duration']
        duration_str = format_duration(duration)
        
        return title, thumbnail_url, duration_str
    else:
        return None, None, None

def format_duration(iso_duration):
    """Convert ISO 8601 duration to human-readable format"""
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(iso_duration)
    if not match:
        return "Unknown duration"
    
    hours, minutes, seconds = match.groups()
    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds:
        parts.append(f"{seconds}s")
    
    return ' '.join(parts) if parts else "0s"

def get_video_transcript(video_id):
    """Fetch transcript using youtube_transcript_api"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Formatting the transcript for display
        transcript_text = "\n".join([f"{entry['start']}s - {entry['start'] + entry['duration']}s: {entry['text']}" for entry in transcript])
        full_text = " ".join([entry['text'] for entry in transcript])
        return transcript, transcript_text, full_text
    except Exception as e:
        return None, f"Error: {str(e)}", None

def sanitize_filename(title):
    """Sanitize the video title to make it a valid filename."""
    # Replace invalid characters with an underscore
    return re.sub(r'[<>:"/\\|?*]', '_', title)

def create_audio_summary(summary_text):
    """Convert summary text to audio and return the file path."""
    tts = gTTS(summary_text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        return temp_audio.name

def remove_emojis(text):
    """Remove emojis from the text using regex"""
    emoji_pattern = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U0001F004-\U0001F0CF\U00002B06-\U00002B07\U000025AA-\U000025AB\U0001F004-\U0001F0CF\U0001F1E6-\U0001F1FF\U00002B50]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def analyze_sentiment(text):
    """Simple sentiment analysis of the transcript"""
    if not text:
        return "Neutral"
    
    positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'love'}
    negative_words = {'bad', 'terrible', 'awful', 'horrible', 'worst', 'sad', 'hate'}
    
    words = [word.lower() for word in nltk.word_tokenize(text) if word.isalpha()]
    word_counts = Counter(words)
    
    positive_score = sum(word_counts[word] for word in positive_words)
    negative_score = sum(word_counts[word] for word in negative_words)
    
    if positive_score > negative_score:
        return "Positive"
    elif negative_score > positive_score:
        return "Negative"
    else:
        return "Neutral"

# Streamlit UI setup
st.set_page_config(page_title="YouTube Video Analyzer", layout="centered")
st.title("🎬 YouTube Video Analyzer")

# Input: YouTube URL
video_url = st.text_input("Enter YouTube Video URL", placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

if video_url:
    video_id = get_video_id(video_url)
    
    # Get video details (title, thumbnail, duration)
    title, thumbnail_url, duration = get_video_details(video_id)
    if title and thumbnail_url:
        st.subheader("🎥 Video Details")
        title_cleaned = remove_emojis(title)  # Clean the title to remove emojis
        st.write(f"**Title**: {title_cleaned}")
        st.image(thumbnail_url, caption=f"Duration: {duration}", use_container_width=True)
        
        # Get transcript of the video
        transcript, transcript_text, full_text = get_video_transcript(video_id)
        if "Error" in transcript_text:
            st.error("Could not fetch transcript: " + transcript_text)
        else:
            # Collapsible transcript section
            with st.expander("📝 View Full Transcript"):
                st.text(transcript_text)
            
            # Sentiment analysis
            if full_text:
                sentiment = analyze_sentiment(full_text)
                st.subheader("Sentiment Analysis")
                st.write(f"The overall sentiment of the video is: **{sentiment}**")
        
        # Video Summary: Using title as the summary
        st.subheader("📄 Video Summary")
        st.write(f"Summary: The video is about {title_cleaned}")
        
        # Audio Summary
        audio_file_path = create_audio_summary(f"The video is about {title_cleaned}")
        st.audio(audio_file_path, format='audio/mp3', start_time=0)
        
        # Download Transcript Button
        st.subheader("📥 Download Transcript")
        if transcript_text != "Error":
            # Sanitize the video title before using it as a filename
            sanitized_title = sanitize_filename(title)
            transcript_file = f"{sanitized_title}_transcript.txt"
            try:
                with open(transcript_file, "w", encoding="utf-8") as file:
                    file.write(transcript_text)
                
                with open(transcript_file, "r", encoding="utf-8") as file:
                    st.download_button(
                        label="Download Transcript",
                        data=file,
                        file_name=transcript_file,
                        mime="text/plain"
                    )
                
                os.remove(transcript_file)  # Clean up the file after download
            except Exception as e:
                st.error(f"Error in file handling: {str(e)}")

else:
    st.info("Please enter a valid YouTube video URL.")