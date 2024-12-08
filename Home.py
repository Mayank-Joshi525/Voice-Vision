import streamlit as st
import pathlib
import requests
import json
from pytube import YouTube
import whisper
from whisper.utils import get_writer
import streamlit_lottie as st_lottie
import streamlit_scrollable_textbox as stx
from utils import *  # Assuming you have this utility file or remove this if unnecessary

# Hide Streamlit's footer
def hide_footer():
    st.markdown("""
        <style>
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

# Function to load a Lottie animation from a URL or a local file
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Streamlit page configuration
st.set_page_config(
        page_title="VOICE VISION",
        page_icon="./assets/favicon.png",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/smaranjitghose/AIAudioTranscriber',
            'Report a bug': "https://github.com/smaranjitghose/AIAudioTranscriber/issues",
            'About': "## A minimalistic application to generate transcriptions for audio built using Python"
        })

if st.button("** NEW **"):
    # Redirect to a different site
    url = "https://your-voice.streamlit.app/"
    st.write("Try Real Time: - [link](%s)" % url)


def main():
    """
    Main Function
    """
    st.title("Transcriber - VOICE VISION")
    hide_footer()

    # Load and display animation
    anim = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_d1ez7q.json")  # Example Lottie URL
    if anim:
        st_lottie(anim, speed=1, reverse=False, loop=True, quality="medium", height=400, width=400, key=None)

    # Initialize Session State Variables
    if "page_index" not in st.session_state:
        st.session_state["page_index"] = 0
        st.session_state["model_path"] = ""
        st.session_state["input_mode"] = ""
        st.session_state["file_path"] = ""
        st.session_state["transcript"] = ""
        st.session_state["lang"] = ""
        st.session_state["segments"] = []

    model_list = {"Artha": r"./assets/models/base.pt",
                  "Dhvani": r"./assets/models/small.pt",
                  "Vaani": r"./assets/models/medium.pt",
                  "General": r"./assets/models/large-v2.pt"}

    # Create a Input Form Component
    input_mode = st.sidebar.selectbox(
        label="Input Mode",
        options=["Youtube Video URL", "Upload Audio File", "Online Audio URL"])
    st.session_state["input_mode"] = input_mode

    # Create a Form Component on the Sidebar for accepting input data and parameters
    with st.sidebar.form(key="input_form", clear_on_submit=False):

        # Nested Component to take user input for audio file as per selected mode
        if input_mode == "Upload Audio File":
            uploaded_file = st.file_uploader(label="Upload your audio📁", type=["wav", "mp3", "m4a"], accept_multiple_files=False)
        elif input_mode == "Youtube Video URL":
            yt_url = st.text_input(label="Paste URL for Youtube Video 📋")
        else:
            aud_url = st.text_input(label="Enter URL for Audio File 🔗 ")

        # Nested Component for model size selection
        model_choice = st.radio(label="Choose Your Transcriber 🪖", options=list(model_list.keys()))
        st.session_state["model_path"] = model_list[model_choice]

        # Nested Optional Component to select segment of the clip to be used for transcription
        extra_configs = st.expander("Choose Segment ✂")
        with extra_configs:
            start = st.number_input("Start time for the media (sec)", min_value=0, step=1)
            duration = st.number_input("Duration (sec) - negative implies till the end", min_value=-1, max_value=30, step=1)

        submitted = st.form_submit_button(label="Generate Transcripts✨")
        if submitted:

            # Create input and output sub-directories
            APP_DIR = pathlib.Path(__file__).parent.absolute()
            INPUT_DIR = APP_DIR / "input"
            INPUT_DIR.mkdir(exist_ok=True)

            # Load Audio from selected Input Source
            if input_mode == "Upload Audio File":
                if uploaded_file is not None:
                    grab_uploaded_file(uploaded_file, INPUT_DIR)
                    get_transcripts()
                else:
                    st.warning("Please🙏 upload a relevant audio file")
            elif input_mode == "Youtube Video URL":
                if yt_url and validate_YT_link(yt_url):
                    grab_youtube_video(yt_url, INPUT_DIR)
                    get_transcripts()
                else:
                    st.warning("Please🙏 enter a valid URL for Youtube video")
            else:
                if aud_url and aud_url.startswith("https://"):
                    grab_youtube_video(aud_url, INPUT_DIR)
                    get_transcripts()
                else:
                    st.warning("Please🙏 enter a valid URL for desired video")

    if st.session_state["transcript"] != "" and st.session_state["lang"] != "":
        col1, col2 = st.columns([4, 4], gap="medium")

        # Display the generated Transcripts
        with col1:
            st.markdown("### Detected language🌐:")
            st.markdown(f"{st.session_state['lang']}")
            st.markdown("### Generated Transcripts📃: ")
            stx.scrollableTextbox(st.session_state["transcript"]["text"], height=300)

        # Display the original Audio
        with col2:
            if st.session_state["input_mode"] == "Youtube Video URL":
                st.markdown("### Youtube Video ▶️")
                st.video(yt_url)
            st.markdown("### Original Audio 🎵")
            with open(st.session_state["file_path"], "rb") as f:
                st.audio(f.read())
            # Download button
            st.markdown("### Save Transcripts📥")
            out_format = st.radio(label="Choose Format", options=["Text File", "SRT File", "VTT File"])
            transcript_download(out_format)


def grab_uploaded_file(uploaded_file, INPUT_DIR: pathlib.Path):
    """
    Method to store the uploaded audio file to server
    """
    try:
        upload_name = uploaded_file.name
        upload_format = upload_name.split(".")[-1]
        input_name = f"audio.{upload_format}"
        st.session_state["file_path"] = INPUT_DIR / input_name
        with open(st.session_state["file_path"], "wb") as f:
            f.write(uploaded_file.read())
    except:
        st.error("😿 Failed to load uploaded audio file")

def grab_youtube_video(url: str, INPUT_DIR: pathlib.Path):
    """
    Method to fetch the audio codec of a Youtube video and save it to server
    """
    try:
        video = YouTube(url).streams.get_by_itag(140).download(INPUT_DIR, filename="audio.mp3")
        st.session_state["file_path"] = INPUT_DIR / "audio.mp3"
    except:
        st.error("😿 Failed to fetch audio from YouTube")

def grab_online_video(url: str, INPUT_DIR: pathlib.Path):
    """
    Method to fetch an online audio file and save it to server
    """
    try:
        r = requests.get(url, allow_redirects=True)
        file_name = url.split("/")[-1]
        file_format = url.split(".")[-1]
        input_name = f"audio.{file_format}"
        st.session_state["file_path"] = INPUT_DIR / input_name
        with open(st.session_state["file_path"], "wb") as f:
            f.write(r.content)
    except:
        st.error("😿 Failed to fetch audio file")


@st.cache_data
def get_model(model_type: str = 'tiny'):
    """
    Method to load Whisper model to disk
    """
    try:
        model = whisper.load_model(model_type)
        return model
    except:
        st.error("😿 Failed to load model")


def get_transcripts():
    """
    Method to generate transcripts for the desired audio file
    """
    try:
        model = get_model()
        audio = whisper.load_audio(st.session_state["file_path"])
        result = model.transcribe(audio)
        st.session_state["transcript"] = result["text"]
        st.session_state["lang"] = match_language(result["language"])
        st.session_state["segments"] = result["segments"]
        st.session_state["transcript"] = result
        st.balloons()
    except:
        st.error("😿 Model Failed to generate transcripts")

def match_language(lang_code: str) -> str:
    """
    Method to match the language code detected by Whisper to full name of the language
    """
    with open("./language.json", "rb") as f:
        lang_data = json.load(f)
    return lang_data[lang_code].capitalize()

def transcript_download(out_format: str):
    """
    Method to save transcripts in VTT format
    """
    APP_DIR = pathlib.Path(__file__).parent.absolute()
    OUTPUT_DIR = APP_DIR / "output"
    OUTPUT_DIR.mkdir(exist_ok=True)

    file_type_dict = {"Text File": "txt", "SRT File": "srt", "VTT File": "vtt"}
    file_type = file_type_dict[out_format]

    if out_format in file_type_dict.keys():
        get_writer(file_type, OUTPUT_DIR)(st.session_state["transcript"], st.session_state["file_path"])
        with open(OUTPUT_DIR / f'audio.{file_type}', "r", encoding="utf-8") as f:
            st.download_button(
                label="Click to download 🔽",
                data=f,
                file_name=f"transcripts.{file_type}",
            )

if __name__ == "__main__":
    main()
