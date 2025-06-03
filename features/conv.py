import streamlit as st
import os
import tempfile
import fitz  # PyMuPDF 
import wave  #Audio file manipulation  
import json
import requests
from vosk import Model, KaldiRecognizer # vosk for offline transcription
import ffmpeg # ** audio video processing ; Open source multimedia framework 
from datetime import datetime

# WhatsApp-like CSS styling
st.markdown("""
<style>
    :root {
        --user-bubble: #DCF8C6;
        --bot-bubble: #FFFFFF;
        --chat-bg: #ECE5DD;
        --header-bg: #075E54;
        --text-dark: #111B21;
        --text-light: #667781;
    }
    
    body {
        background-color: var(--chat-bg);
        font-family: 'Segoe UI', sans-serif;
    }
    
    .chat-header {
        background-color: var(--header-bg);
        color: white;
        padding: 15px;
        position: sticky;
        top: 0;
        z-index: 100;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .chat-container {
        padding: 15px 10px;
        background-color: var(--chat-bg);
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .message {
        max-width: 70%;
        padding: 8px 12px;
        border-radius: 7.5px;
        margin-bottom: 5px;
        position: relative;
        animation: fadeIn 0.3s ease-out;
        word-wrap: break-word;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background-color: var(--user-bubble);
        align-self: flex-end;
        border-bottom-right-radius: 0;
        margin-right: 15px;
        box-shadow: 0 1px 1px rgba(0,0,0,0.1);
    }
    
    .bot-message {
        background-color: var(--bot-bubble);
        align-self: flex-start;
        border-bottom-left-radius: 0;
        margin-left: 15px;
        box-shadow: 0 1px 1px rgba(0,0,0,0.1);
    }
    
    .message-time {
        font-size: 0.7rem;
        color: var(--text-light);
        margin-top: 3px;
        text-align: right;
    }
    
    .bot-message .message-time {
        text-align: left;
    }
    
    .typing-indicator {
        display: inline-flex;
        align-items: center;
        padding: 8px 12px;
        background-color: var(--bot-bubble);
        border-radius: 7.5px;
        margin-left: 15px;
        box-shadow: 0 1px 1px rgba(0,0,0,0.1);
    }
    
    .typing-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: var(--text-light);
        margin: 0 2px;
        animation: typingAnimation 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typingAnimation {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-5px); }
    }
    
    .chat-input-container {
        position: sticky;
        bottom: 0;
        background-color: var(--chat-bg);
        padding: 10px;
        border-top: 1px solid #ddd;
    }
    
    .file-info {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        box-shadow: 0 1px 1px rgba(0,0,0,0.1);
    }
    
    .empty-chat {
        text-align: center;
        padding: 40px 20px;
        color: var(--text-light);
        font-style: italic;
    }
    
    /* Hide Streamlit default elements */
    .stApp > header { display: none; }
    .stApp { background-color: var(--chat-bg); }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

def main():
    
    MODEL_PATH = "vosk-model-small-en-us-0.15" # integration of vosk model
    HUGGINGFACE_API_KEY = "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"

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'processed_text' not in st.session_state:
        st.session_state.processed_text = ""
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False

    # --- Processing functions ---
    def extract_text_from_pdf(file):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def extract_text_from_txt(file):
        return file.read().decode("utf-8")

    def transcribe_audio(file_path):
        model = Model(MODEL_PATH)
        wf = wave.open(file_path, "rb")

        if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
            st.error("Audio file must be mono WAV format")
            return ""

        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()))
        results.append(json.loads(rec.FinalResult()))

        transcript = " ".join([res.get("text", "") for res in results])
        return transcript

    def extract_audio_from_video(video_file):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_vid:
            tmp_vid.write(video_file.read())
            tmp_vid_path = tmp_vid.name

        audio_path = tmp_vid_path.replace(".mp4", ".wav")
        ffmpeg.input(tmp_vid_path).output(audio_path).run()
        return audio_path

    def ask_question_huggingface(context, question):
        API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        
        prompt = f"""
        <|system|>
        You are a helpful AI assistant. Use the provided context to answer the question.
        Context: {context}
        </s>
        <|user|>
        {question}
        </s>
        <|assistant|>
        """
        
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            if response.status_code == 200:
                if isinstance(response.json(), list):
                    return response.json()[0].get('generated_text', 'No response.').split('<|assistant|>')[-1].strip()
                return response.json().get('generated_text', 'No response.').split('<|assistant|>')[-1].strip()
            else:
                return f"❌ Error {response.status_code}: {response.text}"
        except Exception as e:
            return f"❌ Exception occurred: {str(e)}"

    # --- WhatsApp-like UI Structure ---
    
    # Header
    st.markdown("""
    <div class="chat-header">
        <h1>Document Chat Assistant</h1>
    </div>
    """, unsafe_allow_html=True)

    # File upload section
    uploaded_file = st.file_uploader(
        "📁 Upload Document (PDF, TXT, WAV, MP4)", 
        type=["pdf", "txt", "wav", "mp4"],
        key="file_uploader"
    )

    # Process uploaded file
    if uploaded_file and not st.session_state.file_uploaded:
        with st.spinner("Processing your document..."):
            try:
                file_type = uploaded_file.type
                if file_type == "application/pdf":
                    st.session_state.processed_text = extract_text_from_pdf(uploaded_file)
                    file_type_name = "PDF"
                elif file_type == "text/plain":
                    st.session_state.processed_text = extract_text_from_txt(uploaded_file)
                    file_type_name = "Text"
                elif "audio" in file_type:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                        tmp_audio.write(uploaded_file.read())
                        tmp_audio_path = tmp_audio.name
                    st.session_state.processed_text = transcribe_audio(tmp_audio_path)
                    file_type_name = "Audio"
                elif "video" in file_type:
                    audio_path = extract_audio_from_video(uploaded_file)
                    st.session_state.processed_text = transcribe_audio(audio_path)
                    file_type_name = "Video"
                
                st.session_state.file_uploaded = True
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"✅ {file_type_name} document processed successfully! Ask me anything about it.",
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")

    # Show file info if uploaded
    if uploaded_file:
        st.markdown(f"""
        <div class="file-info">
            <b>📄 {uploaded_file.name}</b><br>
            <small>Type: {uploaded_file.type.split('/')[-1].upper()} • Size: {uploaded_file.size / 1024:.1f} KB</small>
        </div>
        """, unsafe_allow_html=True)

    # Chat container - placed above the footer
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        if not st.session_state.messages:
            st.markdown('<div class="empty-chat">👋 Upload a document and start chatting!</div>', unsafe_allow_html=True)
        else:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="message user-message">
                        <div>{message["content"]}</div>
                        <div class="message-time">{message["timestamp"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="message bot-message">
                        <div>{message["content"]}</div>
                        <div class="message-time">{message["timestamp"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat input - stays at bottom above footer
    if st.session_state.file_uploaded:
        if prompt := st.chat_input("Type a message...", key="chat_input"):
            # Add user message to chat history
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            # Show typing indicator
            with chat_container:
                st.markdown("""
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
                """, unsafe_allow_html=True)
            
            # Generate assistant response
            response = ask_question_huggingface(
                st.session_state.processed_text, 
                prompt
            )
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            st.rerun()

    # Document content expander
    if st.session_state.processed_text:
        with st.expander("📄 View Document Content", expanded=False):
            st.text_area(
                "Full Content", 
                st.session_state.processed_text, 
                height=250,
                label_visibility="collapsed"
            )

if __name__ == "__main__":
    main()
