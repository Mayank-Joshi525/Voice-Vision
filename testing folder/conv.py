import streamlit as st
import os
import tempfile
import fitz  # PyMuPDF
import wave
import json
import requests
from vosk import Model, KaldiRecognizer
import ffmpeg

MODEL_PATH = "vosk-model-small-en-us-0.15"
# Get your free API key from https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY = "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"  # Replace with your actual key

# --- Extract text from PDF ---
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# --- Extract text from TXT file ---
def extract_text_from_txt(file):
    return file.read().decode("utf-8")

# --- Transcribe audio using Vosk ---
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

# --- Extract audio from video ---
def extract_audio_from_video(video_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_vid:
        tmp_vid.write(video_file.read())
        tmp_vid_path = tmp_vid.name

    audio_path = tmp_vid_path.replace(".mp4", ".wav")
    ffmpeg.input(tmp_vid_path).output(audio_path).run()
    return audio_path

# --- Ask question using Hugging Face API ---
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
            # The response might be a list of dicts, we take the first generated text
            if isinstance(response.json(), list):
                return response.json()[0].get('generated_text', 'No response.').split('<|assistant|>')[-1].strip()
            return response.json().get('generated_text', 'No response.').split('<|assistant|>')[-1].strip()
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"❌ Exception occurred: {str(e)}"

# --- Streamlit UI ---
st.title("📄 AI-Powered Q&A from PDF/TXT/WAV/MP4")

uploaded_file = st.file_uploader("Upload PDF, TXT, WAV, or MP4", type=["pdf", "txt", "wav", "mp4"])

text_data = ""

if uploaded_file:
    file_type = uploaded_file.type

    try:
        if file_type == "application/pdf":
            text_data = extract_text_from_pdf(uploaded_file)
            st.success("✅ Extracted text from PDF.")
        elif file_type == "text/plain":
            text_data = extract_text_from_txt(uploaded_file)
            st.success("✅ Extracted text from TXT.")
        elif "audio" in file_type:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                tmp_audio.write(uploaded_file.read())
                tmp_audio_path = tmp_audio.name
            text_data = transcribe_audio(tmp_audio_path)
            st.success("✅ Transcribed audio to text.")
        elif "video" in file_type:
            audio_path = extract_audio_from_video(uploaded_file)
            text_data = transcribe_audio(audio_path)
            st.success("✅ Transcribed video to text.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

    # Display extracted text
    if text_data:
        st.subheader("📝 Extracted Content")
        st.text_area("Extracted Text", text_data, height=200)

        st.subheader("❓ Ask a Question")
        user_question = st.text_input("Enter your question")
        if st.button("Get Answer") and user_question:
            with st.spinner("Thinking..."):
                answer = ask_question_huggingface(text_data, user_question)
                st.success(answer)