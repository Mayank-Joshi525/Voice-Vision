# Voice-Vision
Voice Vision is a Python-based virtual voice assistant capable of understanding voice commands and responding with relevant information using speech synthesis. It uses real-time speech recognition and natural language processing to perform tasks such as answering queries using Wikipedia, telling the current time, and more — all through voice interaction.

# Tech Stack
Technology	Purpose
Python 3.x	Core programming language
SpeechRecognition	Speech-to-text conversion
pyttsx3	Text-to-speech output
Wikipedia	Fetching information from the web
datetime	Telling current time
Tkinter (optional)	GUI (if implemented)

# Installation
Clone the repository:
git clone https://github.com/mayank-joshi535/voice-vision.git
cd voice-vision

# Install dependencies:
pip install -r requirements.txt

# install them manually:
pip install SpeechRecognition pyttsx3 wikipedia
Note: You may also need to install PyAudio. If you face issues installing it via pip, refer to platform-specific installation instructions.

# How to Run
python voice_vision.py
You will be prompted to speak. Try commands like:

“What is Python?”

“Tell me about Albert Einstein”

“What time is it?”

# Project Structure
voice-vision/
├── voice_vision.py       # Main script
├── README.md             # Project documentation
├── requirements.txt      # List of dependencies
└── assets/               # (Optional) Images or resources


# Testing
Manual testing was conducted using various test phrases.

Tested across different accents and noise conditions.

Wikipedia search and time announcements were validated with dynamic queries.

#Limitations
Dependent on microphone quality and internet connectivity.

May misinterpret accents or speech in noisy environments.

Limited to English and basic tasks (not a full-fledged AI assistant).
