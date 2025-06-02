# Voice-Vision
Voice Vision is a Python-based virtual voice assistant capable of understanding voice commands and responding with relevant information using speech synthesis. It uses real-time speech recognition and natural language processing to perform tasks such as answering queries using Wikipedia, telling the current time, and more — all through voice interaction.

# Tech Stack
- Technology	Purpose
- Python 3.x	Core programming language
- SpeechRecognition	Speech-to-text conversion
- pyttsx3	Text-to-speech output
- Wikipedia	Fetching information from the web
- datetime	Telling current time
- Streamlit GUI

# Installation
1. Clone the repository:
2. git clone https://github.com/mayank-joshi525/voice-vision.git
3. cd voice-vision
4. streamlit run app.py

# Install dependencies:
- pip install -r requirements.txt

# install them manually:
- pip install SpeechRecognition pyttsx3 wikipedia streamlit
- Note: You may also need to install PyAudio. If you face issues installing it via pip, refer to platform-specific installation instructions.

# How to Run
1. streamlit run app.py
2. You will be prompted to speak. Try commands like:

“What is Python?”

“Tell me about Albert Einstein”

“What time is it?”

# Project Structure
- voice-vision/
- ├── app.py       # Main script
- ├── README.md             # Project documentation
- ├── requirements.txt      # List of dependencies
- └── features/

# Testing
- Manual testing was conducted using various test phrases.

- Tested across different accents and noise conditions.

- Wikipedia search and time announcements were validated with dynamic queries.

# Limitations
- Dependent on microphone quality and internet connectivity.

- May misinterpret accents or speech in noisy environments.

- Limited to English and basic tasks (not a full-fledged AI assistant).

# Contributer
- [Mayank Joshi](https://github.com/mayank-Joshi525/) 
- [Soumya Brajwasi](https://github.com/Somya2427)
- [Paras Joshi](http://github.com/paarasjoshi/)
