import streamlit as st
from googletrans import Translator
from gtts import gTTS
import wikipedia
import pandas as pd
import random
import json
import os
import time
from io import BytesIO

# Initialize translator
translator = Translator()

# Supported languages with their codes
languages = {
    '': 'Select a Language',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'ta': 'Tamil',
    'te': 'Telugu',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'pa': 'Punjabi',
    'ur': 'Urdu',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh-cn': 'Chinese (Simplified)',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'tr': 'Turkish',
    'nl': 'Dutch',
    'pl': 'Polish'
}

# Reverse lookup from value to key
lang_code_map = {v: k for k, v in languages.items()}

# Fetch Wikipedia intro for language
def fetch_language_info(lang_name):
    search_titles = [
        f"{lang_name} language",
        f"{lang_name} alphabet",
        f"{lang_name} script",
        lang_name
    ]
    for title in search_titles:
        try:
            return wikipedia.summary(title, sentences=4)
        except:
            continue
    return "❗Sorry, no detailed information found for this language on Wikipedia."

# Translation logic
def translate_text(text, dest_lang):
    try:
        result = translator.translate(text, dest=dest_lang)
        return result.text
    except Exception:
        return "⚠️ Translation failed."

# Text-to-speech audio
def generate_audio(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception:
        return None

# Common phrases by level
def get_common_phrases(level):
    phrases = {
        "beginner": [
            "Hello", "Thank you", "Please", "How are you?", "My name is...", 
            "Where is...?", "How much?", "I don't understand", "Help me please", 
            "Goodbye", "Yes", "No", "Excuse me", "I'm sorry", "Good morning"
        ],
        "intermediate": [
            "What do you do for work?", "I've been learning for three months", 
            "Could you speak more slowly?", "I would like to order...", 
            "What's the weather like today?", "Can you recommend a good restaurant?",
            "Where are you from?", "How long have you been here?",
            "I'm interested in...", "It was nice meeting you"
        ],
        "advanced": [
            "I'm considering a career change", "The cultural implications are fascinating",
            "That reminds me of something I read recently", "I'd appreciate your perspective on this matter",
            "Let's discuss the underlying issues", "That's an interesting point of view",
            "I've been contemplating this topic", "What would be the long-term consequences?",
            "There are several factors to consider", "I see both sides of the argument"
        ]
    }
    return phrases.get(level, [])

# Generate vocabulary lists by category
def get_vocabulary_by_category(category):
    vocabulary = {
        "greetings": ["Hello", "Good morning", "Good afternoon", "Good evening", "Welcome", "Hi", "Hey", "Greetings"],
        "food": ["Bread", "Rice", "Meat", "Fish", "Vegetable", "Fruit", "Water", "Juice", "Coffee", "Tea", "Restaurant", "Menu", "Delicious"],
        "travel": ["Airport", "Train", "Bus", "Ticket", "Hotel", "Passport", "Luggage", "Map", "Tourist", "Vacation", "Trip", "Journey"],
        "family": ["Mother", "Father", "Sister", "Brother", "Son", "Daughter", "Grandparent", "Cousin", "Aunt", "Uncle", "Family", "Child"],
        "numbers": ["One", "Two", "Three", "Four", "Five", "Ten", "Twenty", "Hundred", "Thousand", "First", "Second", "Third"],
        "time": ["Day", "Week", "Month", "Year", "Today", "Tomorrow", "Yesterday", "Morning", "Evening", "Night", "Hour", "Minute"]
    }
    return vocabulary.get(category, [])

# Quiz generator for vocabulary practice
def generate_quiz(language_code, category, num_questions=5):
    words = get_vocabulary_by_category(category)
    if len(words) < num_questions:
        num_questions = len(words)
    
    quiz_words = random.sample(words, num_questions)
    quiz = []
    
    for word in quiz_words:
        translated = translate_text(word, language_code)
        options = [translated]
        
        # Generate wrong options
        other_words = [w for w in words if w != word]
        if len(other_words) >= 3:
            wrong_words = random.sample(other_words, 3)
            for wrong in wrong_words:
                options.append(translate_text(wrong, language_code))
        else:
            # If not enough words in category, use random translations
            for _ in range(3):
                random_word = random.choice(["Apple", "House", "Book", "Car", "Tree", "Sun", "Moon", "Star", "Dog", "Cat"])
                options.append(translate_text(random_word, language_code))
        
        random.shuffle(options)
        correct_index = options.index(translated)
        
        quiz.append({
            "question": f"What does '{word}' mean in {languages[language_code]}?",
            "options": options,
            "correct": correct_index,
            "english": word,
            "translated": translated
        })
    
    return quiz

# Practice conversation generator
def generate_practice_conversation(level, language_code):
    conversations = {
        "beginner": [
            {"role": "A", "text": "Hello! How are you?"},
            {"role": "B", "text": "I'm fine, thank you. And you?"},
            {"role": "A", "text": "I'm good. What's your name?"},
            {"role": "B", "text": "My name is Maria. Nice to meet you."},
            {"role": "A", "text": "Nice to meet you too, Maria."}
        ],
        "intermediate": [
            {"role": "A", "text": "Excuse me, do you know how to get to the museum?"},
            {"role": "B", "text": "Yes, you can take bus number 5 or walk for about 15 minutes."},
            {"role": "A", "text": "How often does the bus run?"},
            {"role": "B", "text": "Every 20 minutes. There's a bus stop just around the corner."},
            {"role": "A", "text": "Great, thank you for your help!"},
            {"role": "B", "text": "You're welcome. Enjoy your visit!"}
        ],
        "advanced": [
            {"role": "A", "text": "I've been thinking about taking a cooking class. Have you ever tried one?"},
            {"role": "B", "text": "Yes, I attended a six-week course last year. It was an incredible experience."},
            {"role": "A", "text": "What kind of dishes did you learn to prepare?"},
            {"role": "B", "text": "We focused on Mediterranean cuisine, with emphasis on sustainable ingredients."},
            {"role": "A", "text": "That sounds fascinating. Would you recommend the same course?"},
            {"role": "B", "text": "Absolutely, though there are many specialized options depending on your interests."}
        ]
    }
    
    convo = conversations.get(level, conversations["beginner"])
    translated_convo = []
    
    for line in convo:
        translated = translate_text(line["text"], language_code)
        translated_convo.append({
            "role": line["role"],
            "original": line["text"],
            "translated": translated
        })
    
    return translated_convo

# Function to get basic grammar rules
def get_grammar_rules(language_code):
    # This would ideally be expanded with actual grammar rules for each language
    grammar_rules = {
        "es": [
            "Spanish nouns have gender (masculine or feminine)",
            "Adjectives must match the gender and number of the noun they modify",
            "Verb conjugations change based on the subject (yo, tú, él/ella, etc.)",
            "The most common tenses for beginners are present, past (preterite), and future"
        ],
        "fr": [
            "French nouns have gender (masculine or feminine)",
            "Adjectives must agree in gender and number with the nouns they modify",
            "French has formal and informal ways of addressing people (tu vs. vous)",
            "Pronunciation is key - many letters are silent at the end of words"
        ],
        "de": [
            "German has three grammatical genders: masculine, feminine, and neuter",
            "German uses four cases: nominative, accusative, dative, and genitive",
            "Word order is flexible but the verb is usually in the second position in a sentence",
            "Nouns in German are always capitalized"
        ],
        "ja": [
            "Japanese sentences follow Subject-Object-Verb order",
            "Particles (は, が, を, etc.) mark the grammatical function of words",
            "Verbs don't change for person or number, but they conjugate for tense and politeness",
            "Japanese doesn't use spaces between words"
        ],
        "zh-cn": [
            "Chinese doesn't conjugate verbs for tense or person",
            "Word order is typically Subject-Verb-Object",
            "Measure words are used when counting objects",
            "Tones are crucial for correct pronunciation and meaning"
        ]
    }
    
    # For languages without specific rules, return general language learning tips
    default_rules = [
        "Focus on learning the most common 500-1000 words first",
        "Practice speaking from day one, even if it feels uncomfortable",
        "Listen to native speakers through music, podcasts, or videos",
        "Try to study a little bit every day rather than cramming"
    ]
    
    return grammar_rules.get(language_code, default_rules)

# Learning path roadmap generator
def generate_learning_path(language_code):
    language_name = languages[language_code]
    
    beginner_milestones = [
        f"Learn the basic alphabet and pronunciation of {language_name}",
        f"Master 100 essential {language_name} words",
        "Learn basic greetings and introductions",
        "Practice simple conversations",
        "Understand basic grammar concepts"
    ]
    
    intermediate_milestones = [
        "Expand vocabulary to 500-1000 words",
        "Practice past, present, and future tenses",
        "Hold conversations on everyday topics",
        "Begin reading simple texts",
        "Practice listening comprehension with native content"
    ]
    
    advanced_milestones = [
        "Refine pronunciation and accent",
        "Master complex grammar structures",
        "Understand idioms and cultural references",
        "Read newspapers and watch shows without subtitles",
        "Engage in debates and complex discussions"
    ]
    
    return {
        "beginner": beginner_milestones,
        "intermediate": intermediate_milestones,
        "advanced": advanced_milestones
    }

# Pronunciation guide
def get_pronunciation_tips(language_code):
    tips = {
        "es": [
            "The letter 'h' is always silent",
            "The letter 'j' sounds like the English 'h' but stronger",
            "The letter 'ñ' is pronounced like 'ny' in 'canyon'",
            "The letter 'r' is rolled at the beginning of words"
        ],
        "fr": [
            "The letter 'r' is pronounced in the back of the throat",
            "Final consonants are often silent",
            "Nasal vowels are pronounced through the nose",
            "The letter combinations 'ai' and 'ei' sound like 'eh'"
        ],
        "de": [
            "The letter 'ch' has no English equivalent (like the 'ch' in 'loch')",
            "The letter 'v' is pronounced like 'f'",
            "The letter 'w' is pronounced like 'v'",
            "Umlauts (ä, ö, ü) change the sound of the vowel significantly"
        ],
        "ja": [
            "Japanese has a syllabary system, not an alphabet",
            "Each character (hiragana/katakana) represents a syllable, not a single sound",
            "The 'r' sound is between the English 'r' and 'l'",
            "Pitch accent is important but subtle"
        ],
        "zh-cn": [
            "Mandarin Chinese has four main tones plus a neutral tone",
            "The same syllable with different tones can have completely different meanings",
            "Some sounds like 'q', 'x', and 'zh' don't exist in English",
            "Practice with tone pairs (two tones in sequence) to improve fluency"
        ]
    }
    
    default_tips = [
        "Listen carefully to native speakers",
        "Practice mouth and tongue positions for unfamiliar sounds",
        "Record yourself speaking and compare to native audio",
        "Focus on rhythm and intonation, not just individual sounds"
    ]
    
    return tips.get(language_code, default_tips)

# Progress tracking functionality
def save_progress(username, language_code, activity, score=None):
    if not os.path.exists("user_progress"):
        os.makedirs("user_progress")
        
    filename = f"user_progress/{username}_{language_code}.json"
    
    # Load existing progress
    progress = {}
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                progress = json.load(file)
        except:
            progress = {}
    
    # Initialize if needed
    if "activities" not in progress:
        progress["activities"] = []
    if "scores" not in progress:
        progress["scores"] = {}
    if "stats" not in progress:
        progress["stats"] = {
            "words_learned": 0,
            "exercises_completed": 0,
            "practice_sessions": 0,
            "last_active": ""
        }
    
    # Update progress
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    progress["activities"].append({"activity": activity, "timestamp": timestamp})
    progress["stats"]["last_active"] = timestamp
    
    if activity == "vocabulary":
        progress["stats"]["words_learned"] += 5
    elif activity == "exercise":
        progress["stats"]["exercises_completed"] += 1
    elif activity == "practice":
        progress["stats"]["practice_sessions"] += 1
    
    if score is not None:
        if activity not in progress["scores"]:
            progress["scores"][activity] = []
        progress["scores"][activity].append({"score": score, "timestamp": timestamp})
    
    # Save progress
    with open(filename, "w") as file:
        json.dump(progress, file)
    
    return progress

# Get user progress
def get_progress(username, language_code):
    filename = f"user_progress/{username}_{language_code}.json"
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except:
            return None
    return None

# Streamlit UI
st.set_page_config(page_title="Language Learner Pro", layout="wide")

# Session state initialization
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'quiz_results' not in st.session_state:
    st.session_state.quiz_results = None
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_answered' not in st.session_state:
    st.session_state.quiz_answered = []
if 'show_flashcards' not in st.session_state:
    st.session_state.show_flashcards = False
if 'flashcard_index' not in st.session_state:
    st.session_state.flashcard_index = 0
if 'flashcard_flipped' not in st.session_state:
    st.session_state.flashcard_flipped = False
if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = None

# Login/User section
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/language.png", width=100)
    st.title("Language Learner Pro")
    
    if not st.session_state.username:
        st.subheader("👤 User Profile")
        username = st.text_input("Enter your username:")
        if st.button("Set Username"):
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
            st.rerun()
    else:
        st.subheader(f"👋 Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.username = ""
            st.rerun()

# Main app content
if st.session_state.username:
    st.title("🌍 Language Learner Pro")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📚 Learn", 
        "🔤 Vocabulary", 
        "🎯 Practice", 
        "🎮 Quiz", 
        "🗣️ Pronunciation", 
        "🧠 Grammar", 
        "📊 Progress"
    ])
    
    # Language selection in sidebar
    with st.sidebar:
        language_choice = st.selectbox(
            "Choose a Language to Learn", 
            list(languages.values()),
            index=0
        )
        language_code = lang_code_map.get(language_choice, '')
        
        if language_code:
            # Show learning level selection
            level = st.radio(
                "Select your level:",
                ["Beginner", "Intermediate", "Advanced"],
                horizontal=True
            )
            level = level.lower()
            
            # Show quick stats if available
            progress = get_progress(st.session_state.username, language_code)
            if progress:
                st.divider()
                st.subheader("Quick Stats")
                stats = progress["stats"]
                st.caption(f"Words learned: {stats['words_learned']}")
                st.caption(f"Exercises completed: {stats['exercises_completed']}")
                st.caption(f"Practice sessions: {stats['practice_sessions']}")
                st.caption(f"Last active: {stats['last_active']}")
    
    # Learn tab
    with tab1:
        if language_code:
            st.header(f"📚 Learning {language_choice}")
            
            # Language information
            with st.expander("About this language", expanded=True):
                info = fetch_language_info(language_choice)
                st.write(info)
            
            # Learning path
            with st.expander("Your Learning Path", expanded=True):
                learning_path = generate_learning_path(language_code)
                
                st.subheader("Beginner Milestones")
                for i, milestone in enumerate(learning_path["beginner"]):
                    st.markdown(f"- {milestone}")
                
                st.subheader("Intermediate Milestones")
                for i, milestone in enumerate(learning_path["intermediate"]):
                    st.markdown(f"- {milestone}")
                
                st.subheader("Advanced Milestones")
                for i, milestone in enumerate(learning_path["advanced"]):
                    st.markdown(f"- {milestone}")
            
            # Basic translation
            st.subheader("✍️ Translate a Sentence")
            col1, col2 = st.columns([1, 1])
            with col1:
                english_input = st.text_input("Enter English", placeholder="Type something...")
            with col2:
                if english_input:
                    translated_text = translate_text(english_input, language_code)
                    st.text_input(f"Translated ({language_choice})", value=translated_text, disabled=True)
            
            # Audio pronunciation
            if english_input:
                col3, col4 = st.columns([1, 1])
                with col3:
                    st.markdown("🔊 English Audio")
                    audio_en = generate_audio(english_input, 'en')
                    if audio_en:
                        st.audio(audio_en, format='audio/mp3')
                with col4:
                    st.markdown(f"🔊 {language_choice} Audio")
                    audio_lang = generate_audio(translated_text, language_code)
                    if audio_lang:
                        st.audio(audio_lang, format='audio/mp3')
            
            # Common phrases by level
            st.subheader(f"📝 Common {level.capitalize()} Phrases")
            phrases = get_common_phrases(level)
            for phrase in phrases:
                translated = translate_text(phrase, language_code) 
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.text(phrase)
                with col2:
                    st.text(translated)
                with col3:
                    audio = generate_audio(translated, language_code)
                    if audio:
                        st.audio(audio, format='audio/mp3')
        else:
            st.info("Please select a language to begin learning.")
    
    # Vocabulary tab
    with tab2:
        if language_code:
            st.header(f"🔤 {language_choice} Vocabulary")
            
            # Category selection
            category = st.selectbox(
                "Select vocabulary category:",
                ["greetings", "food", "travel", "family", "numbers", "time"]
            )
            
            # Display mode selection
            display_mode = st.radio(
                "Display mode:",
                ["List View", "Flashcards"],
                horizontal=True
            )
            
            words = get_vocabulary_by_category(category)
            
            if display_mode == "List View":
                for word in words:
                    translated = translate_text(word, language_code)
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.text(word)
                    with col2:
                        st.text(translated)
                    with col3:
                        audio = generate_audio(translated, language_code)
                        if audio:
                            st.audio(audio, format='audio/mp3')
                
                if st.button("Mark these words as learned"):
                    save_progress(st.session_state.username, language_code, "vocabulary")
                    st.success(f"Added {len(words)} words to your learned vocabulary!")
            
            else:  # Flashcards
                if not st.session_state.show_flashcards:
                    if st.button("Start Flashcards"):
                        st.session_state.show_flashcards = True
                        st.session_state.flashcard_index = 0
                        st.session_state.flashcard_flipped = False
                        st.rerun()
                else:
                    # Prepare translated words once
                    if 'flashcard_words' not in st.session_state:
                        st.session_state.flashcard_words = []
                        for word in words:
                            translated = translate_text(word, language_code)
                            st.session_state.flashcard_words.append({
                                "english": word,
                                "translated": translated
                            })
                    
                    # Display current flashcard
                    current = st.session_state.flashcard_words[st.session_state.flashcard_index]
                    
                    # Flashcard container with fixed height
                    card_container = st.container()
                    card_container.markdown(
                        f"""
                        <div style="
                            height: 200px;
                            background-color: white;
                            border-radius: 10px;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            margin-bottom: 20px;
                            padding: 20px;
                            text-align: center;
                            font-size: 24px;
                        ">
                            <p>{current['translated'] if st.session_state.flashcard_flipped else current['english']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Audio for current word
                    audio_word = current['translated'] if st.session_state.flashcard_flipped else current['english']
                    audio_lang = language_code if st.session_state.flashcard_flipped else 'en'
                    audio = generate_audio(audio_word, audio_lang)
                    if audio:
                        st.audio(audio, format='audio/mp3')
                    
                    # Controls
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        if st.button("Previous", disabled=st.session_state.flashcard_index == 0):
                            st.session_state.flashcard_index -= 1
                            st.session_state.flashcard_flipped = False
                            st.rerun()
                    
                    with col2:
                        if st.button("Flip Card"):
                            st.session_state.flashcard_flipped = not st.session_state.flashcard_flipped
                            st.rerun()
                    
                    with col3:
                        if st.button("Next", disabled=st.session_state.flashcard_index == len(words) - 1):
                            st.session_state.flashcard_index += 1
                            st.session_state.flashcard_flipped = False
                            st.rerun()
                    
                    # Exit flashcards
                    if st.button("Exit Flashcards"):
                        st.session_state.show_flashcards = False
                        if 'flashcard_words' in st.session_state:
                            del st.session_state.flashcard_words
                        st.rerun()
        else:
            st.info("Please select a language to explore vocabulary.")
    
    # Practice tab
    with tab3:
        if language_code:
            st.header(f"🎯 {language_choice} Practice")
            
            # Practice conversational patterns
            st.subheader("Practice Conversations")
            
            if st.session_state.current_conversation is None and st.button("Generate Conversation"):
                st.session_state.current_conversation = generate_practice_conversation(level, language_code)
                save_progress(st.session_state.username, language_code, "practice")
                st.rerun()
            
            if st.session_state.current_conversation:
                # Display conversation
                for i, line in enumerate(st.session_state.current_conversation):
                    with st.container():
                        col1, col2 = st.columns([1, 10])
                        with col1:
                            st.markdown(f"**{line['role']}:**")
                        with col2:
                            st.markdown(f"{line['original']}")
                            st.markdown(f"*{line['translated']}*")
                        
                        # Audio for each line
                        col3, col4 = st.columns([5, 5])
                        with col3:
                            en_audio = generate_audio(line['original'], 'en')
                            if en_audio:
                                st.audio(en_audio, format='audio/mp3')
                        with col4:
                            lang_audio = generate_audio(line['translated'], language_code)
                            if lang_audio:
                                st.audio(lang_audio, format='audio/mp3')
                
                # Practice options
                st.subheader("Practice this conversation")
                practice_mode = st.radio(
                    "Choose practice mode:",
                    ["Listen and Repeat", "Memory Practice", "Role Play"],
                    horizontal=True
                )
                
                if practice_mode == "Listen and Repeat":
                    st.write("Listen to each line and repeat it aloud to practice pronunciation.")
                    
                elif practice_mode == "Memory Practice":
                    st.write("Try to recall the translation before revealing it.")
                    selected_line = st.slider("Select line to practice:", 0, len(st.session_state.current_conversation)-1)
                    
                    line = st.session_state.current_conversation[selected_line]
                    st.markdown(f"**English:** {line['original']}")
                    
                    if st.button("Show Translation"):
                        st.markdown(f"**{language_choice}:** {line['translated']}")
                        lang_audio = generate_audio(line['translated'], language_code)
                        if lang_audio:
                            st.audio(lang_audio, format='audio/mp3')
                
                elif practice_mode == "Role Play":
                    st.write("Practice role-playing this conversation. Choose your role:")
                    role = st.radio("Your role:", ["A", "B"], horizontal=True)
                    
                    st.write("The app will show the other role's lines. Try to respond appropriately before seeing your lines.")
                    for line in st.session_state.current_conversation:
                        if line['role'] != role:
                            st.markdown(f"**{line['role']}:** *{line['translated']}*")
                            lang_audio = generate_audio(line['translated'], language_code)
                            if lang_audio:
                                st.audio(lang_audio, format='audio/mp3')
                        else:
                            st.markdown("**Your turn to speak...**")
                            if st.button(f"Show my line {line['role']}", key=f"show_{line['role']}_{st.session_state.current_conversation.index(line)}"):
                                st.markdown(f"**You ({role}):** *{line['translated']}*")
                                st.markdown(f"(English: {line['original']})")
                
                if st.button("Generate New Conversation"):
                    st.session_state.current_conversation = generate_practice_conversation(level, language_code)
                    save_progress(st.session_state.username, language_code, "practice")
                    st.rerun()
        else:
            st.info("Please select a language to practice conversations.")
    
    # Quiz tab
    with tab4:
        if language_code:
            st.header(f"🎮 {language_choice} Quiz")
            
            if st.session_state.current_quiz is None:
                # Quiz category selection
                quiz_category = st.selectbox(
                    "Select vocabulary category for quiz:",
                    ["greetings", "food", "travel", "family", "numbers", "time"]
                )
                
                quiz_length = st.slider("Number of questions:", 5, 20, 10)
                
                if st.button("Start Quiz"):
                    st.session_state.current_quiz = generate_quiz(language_code, quiz_category, quiz_length)
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_answered = [False] * len(st.session_state.current_quiz)
                    st.rerun()
            else:
                # Display quiz
                progress_bar = st.progress(0)
                
                # Calculate progress
                answered_count = sum(st.session_state.quiz_answered)
                total_questions = len(st.session_state.current_quiz)
                progress = answered_count / total_questions
                progress_bar.progress(progress)
                
                st.write(f"Score: {st.session_state.quiz_score}/{total_questions}")
                
                # Display each question
                for i, question in enumerate(st.session_state.current_quiz):
                    with st.container():
                        st.subheader(f"Question {i+1}")
                        st.write(question["question"])
                        
                        # Add audio for the word
                        audio = generate_audio(question["english"], 'en')
                        if audio:
                            st.audio(audio, format='audio/mp3')
                        
                        # If already answered, show result
                        if st.session_state.quiz_answered[i]:
                            selected_option = st.radio(
                                "Options:",
                                question["options"],
                                index=st.session_state.quiz_results[i]["selected"],
                                disabled=True
                            )
                            
                            if st.session_state.quiz_results[i]["correct"]:
                                st.success("Correct! ✅")
                            else:
                                st.error(f"Incorrect ❌ - The correct answer is: {question['options'][question['correct']]}")
                                
                            # Show translation audio
                            audio = generate_audio(question["translated"], language_code)
                            if audio:
                                st.audio(audio, format='audio/mp3')
                        else:
                            # Not answered yet
                            selected_option = st.radio(
                                "Choose the correct translation:",
                                question["options"],
                                key=f"quiz_q{i}"
                            )
                            
                            if st.button("Submit", key=f"submit_q{i}"):
                                selected_index = question["options"].index(selected_option)
                                is_correct = selected_index == question["correct"]
                                
                                # Update score and tracking
                                if is_correct:
                                    st.session_state.quiz_score += 1
                                
                                if "quiz_results" not in st.session_state:
                                    st.session_state.quiz_results = []
                                
                                # Extend quiz_results list if needed
                                while st.session_state.get('quiz_results', []) and len(st.session_state.quiz_results) > i:                         
                                    st.session_state.quiz_results.append(None)
                                    
                                    st.session_state.quiz_results[i] = {
                                    "selected": selected_index,
                                    "correct": is_correct
                                }
                                
                                st.session_state.quiz_answered[i] = True
                                
                                # Save progress if this was the last question
                                if all(st.session_state.quiz_answered):
                                    final_score = st.session_state.quiz_score / total_questions * 100
                                    save_progress(
                                        st.session_state.username, 
                                        language_code, 
                                        "quiz", 
                                        final_score
                                    )
                                
                                st.rerun()
                
                # Option to end quiz early
                if st.button("Finish Quiz"):
                    if not all(st.session_state.quiz_answered):
                        # Only save progress if not all questions were answered
                        answered = sum(st.session_state.quiz_answered)
                        if answered > 0:
                            final_score = st.session_state.quiz_score / answered * 100
                            save_progress(
                                st.session_state.username, 
                                language_code, 
                                "quiz", 
                                final_score
                            )
                    
                    # Reset quiz state
                    st.session_state.current_quiz = None
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_answered = []
                    st.session_state.quiz_results = None
                    st.rerun()
        else:
            st.info("Please select a language to take a quiz.")
    
    # Pronunciation tab
    with tab5:
        if language_code:
            st.header(f"🗣️ {language_choice} Pronunciation")
            
            # Pronunciation tips
            with st.expander("Pronunciation Tips", expanded=True):
                tips = get_pronunciation_tips(language_code)
                for tip in tips:
                    st.markdown(f"- {tip}")
            
            # Pronunciation practice
            st.subheader("Practice Pronunciation")
            
            # Select practice mode
            practice_mode = st.radio(
                "Choose practice mode:",
                ["Word by Word", "Sentence Practice", "Tongue Twisters"],
                horizontal=True
            )
            
            if practice_mode == "Word by Word":
                # Get vocabulary from a category
                category = st.selectbox(
                    "Select vocabulary category:",
                    ["greetings", "food", "travel", "family", "numbers", "time"],
                    key="pron_category"
                )
                
                words = get_vocabulary_by_category(category)
                
                # Display words with slow and normal pronunciation
                for word in words[:10]:  # Limit to 10 words for better performance
                    translated = translate_text(word, language_code)
                    
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.markdown(f"**{word}**")
                    with col2:
                        st.markdown(f"*{translated}*")
                    with col3:
                        audio = generate_audio(translated, language_code)
                        if audio:
                            st.audio(audio, format='audio/mp3')
                    
                    st.write("Practice saying this word multiple times.")
                    st.divider()
            
            elif practice_mode == "Sentence Practice":
                # Practice with sentences
                sample_sentences = [
                    "My name is...",
                    "Where is the nearest restaurant?",
                    "I would like to order coffee, please.",
                    "What time does the train arrive?",
                    "Can you help me find my way to the hotel?"
                ]
                
                selected_sentence = st.selectbox(
                    "Choose a sentence to practice:",
                    sample_sentences
                )
                
                translated_sentence = translate_text(selected_sentence, language_code)
                
                st.markdown(f"**English:** {selected_sentence}")
                st.markdown(f"**{language_choice}:** {translated_sentence}")
                
                # Audio controls
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("🔊 Listen:")
                    audio = generate_audio(translated_sentence, language_code)
                    if audio:
                        st.audio(audio, format='audio/mp3')
                
                with col2:
                    st.markdown("🎤 Practice:")
                    st.write("Repeat the sentence aloud several times")
                
                # Custom sentence input
                st.write("Or try your own sentence:")
                custom_sentence = st.text_input("Enter a sentence in English:", key="custom_sentence")
                if custom_sentence:
                    translated_custom = translate_text(custom_sentence, language_code)
                    st.markdown(f"**{language_choice}:** {translated_custom}")
                    audio_custom = generate_audio(translated_custom, language_code)
                    if audio_custom:
                        st.audio(audio_custom, format='audio/mp3')
            
            elif practice_mode == "Tongue Twisters":
                st.write("Tongue twisters help practice difficult sounds. Try these:")
                
                # Some common tongue twisters in English
                tongue_twisters = [
                    "She sells seashells by the seashore.",
                    "Peter Piper picked a peck of pickled peppers.",
                    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
                    "Red lorry, yellow lorry.",
                    "Unique New York."
                ]
                
                selected_twister = st.selectbox(
                    "Choose a tongue twister:",
                    tongue_twisters
                )
                
                # Translate the tongue twister
                translated_twister = translate_text(selected_twister, language_code)
                
                st.markdown(f"**English:** {selected_twister}")
                st.markdown(f"**{language_choice}:** {translated_twister}")
                
                # Audio for tongue twister
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("🔊 English:")
                    audio_en = generate_audio(selected_twister, 'en')
                    if audio_en:
                        st.audio(audio_en, format='audio/mp3')
                
                with col2:
                    st.markdown(f"🔊 {language_choice}:")
                    audio_lang = generate_audio(translated_twister, language_code)
                    if audio_lang:
                        st.audio(audio_lang, format='audio/mp3')
                
                st.write("Practice by saying the tongue twister slowly at first, then gradually increase your speed.")
        else:
            st.info("Please select a language to practice pronunciation.")
    
    # Grammar tab
    with tab6:
        if language_code:
            st.header(f"🧠 {language_choice} Grammar")
            
            # Grammar rules
            with st.expander("Basic Grammar Rules", expanded=True):
                rules = get_grammar_rules(language_code)
                for rule in rules:
                    st.markdown(f"- {rule}")
            
            # Grammar exercises based on level
            st.subheader("Grammar Practice")
            
            exercise_types = ["Fill in the blanks", "Multiple choice", "Sentence building"]
            exercise_type = st.selectbox("Exercise type:", exercise_types)
            
            if exercise_type == "Fill in the blanks":
                # Simple fill in the blanks exercises
                exercises = {
                    "beginner": [
                        {
                            "sentence": "My name ___ John.",
                            "options": ["is", "am", "are", "be"],
                            "correct": "is",
                            "explanation": "Use 'is' with third-person singular (he, she, it)."
                        },
                        {
                            "sentence": "They ___ students.",
                            "options": ["is", "am", "are", "be"],
                            "correct": "are",
                            "explanation": "Use 'are' with plural subjects."
                        }
                    ],
                    "intermediate": [
                        {
                            "sentence": "I ___ lived here for two years.",
                            "options": ["have", "has", "am", "was"],
                            "correct": "have",
                            "explanation": "Use 'have' with first-person in present perfect tense."
                        },
                        {
                            "sentence": "If it ___ tomorrow, we'll stay home.",
                            "options": ["rains", "will rain", "rained", "raining"],
                            "correct": "rains",
                            "explanation": "In conditional sentences, use present tense in the if-clause."
                        }
                    ],
                    "advanced": [
                        {
                            "sentence": "I wish I ___ speak five languages.",
                            "options": ["could", "can", "will", "would"],
                            "correct": "could",
                            "explanation": "After 'wish', use past tense or 'could' for present wishes."
                        },
                        {
                            "sentence": "By next year, they ___ the project.",
                            "options": ["will have completed", "will complete", "have completed", "complete"],
                            "correct": "will have completed",
                            "explanation": "Future perfect tense is used for actions that will be completed by a certain time."
                        }
                    ]
                }
                
                current_exercises = exercises.get(level, exercises["beginner"])
                
                for i, exercise in enumerate(current_exercises):
                    st.write(f"**Exercise {i+1}:** {exercise['sentence']}")
                    answer = st.radio(
                        "Choose the correct option:",
                        exercise["options"],
                        key=f"grammar_ex_{i}"
                    )
                    
                    check_button = st.button("Check Answer", key=f"check_grammar_{i}")
                    
                    if check_button:
                        if answer == exercise["correct"]:
                            st.success("Correct! ✅")
                        else:
                            st.error(f"Incorrect. The correct answer is: {exercise['correct']}")
                        
                        st.info(f"Explanation: {exercise['explanation']}")
                        
                        # Translate the correct sentence
                        full_sentence = exercise["sentence"].replace("___", exercise["correct"])
                        translated = translate_text(full_sentence, language_code)
                        st.write(f"Translation: {translated}")
                        
                        # Audio for the translated sentence
                        audio = generate_audio(translated, language_code)
                        if audio:
                            st.audio(audio, format='audio/mp3')
            
            elif exercise_type == "Multiple choice":
                # Simple multiple choice grammar questions
                questions = {
                    "beginner": [
                        {
                            "question": "Which sentence is correct?",
                            "options": [
                                "She don't like coffee.",
                                "She doesn't like coffee.",
                                "She not like coffee.",
                                "She do not likes coffee."
                            ],
                            "correct": "She doesn't like coffee.",
                            "explanation": "For third-person singular negative in present simple, use 'doesn't' + base verb."
                        }
                    ],
                    "intermediate": [
                        {
                            "question": "Which sentence uses the past perfect correctly?",
                            "options": [
                                "I had finished my homework before dinner.",
                                "I have finished my homework before dinner.",
                                "I was finished my homework before dinner.",
                                "I finished my homework before dinner had."
                            ],
                            "correct": "I had finished my homework before dinner.",
                            "explanation": "Past perfect (had + past participle) is used for an action completed before another past action."
                        }
                    ],
                    "advanced": [
                        {
                            "question": "Which sentence contains a correct conditional structure?",
                            "options": [
                                "If I would have known, I would have told you.",
                                "If I had known, I would told you.",
                                "If I had known, I would have told you.",
                                "If I would know, I would have told you."
                            ],
                            "correct": "If I had known, I would have told you.",
                            "explanation": "In third conditional (past impossible situations), use 'if + past perfect' and 'would have + past participle'."
                        }
                    ]
                }
                
                current_questions = questions.get(level, questions["beginner"])
                
                for i, question in enumerate(current_questions):
                    st.write(f"**Question {i+1}:** {question['question']}")
                    answer = st.radio(
                        "Choose the correct option:",
                        question["options"],
                        key=f"mc_grammar_{i}"
                    )
                    
                    check_button = st.button("Check Answer", key=f"check_mc_{i}")
                    
                    if check_button:
                        if answer == question["correct"]:
                            st.success("Correct! ✅")
                        else:
                            st.error(f"Incorrect. The correct answer is: {question['correct']}")
                        
                        st.info(f"Explanation: {question['explanation']}")
                        
                        # Translate the correct sentence
                        translated = translate_text(question["correct"], language_code)
                        st.write(f"Translation: {translated}")
                        
                        # Audio for the translated sentence
                        audio = generate_audio(translated, language_code)
                        if audio:
                            st.audio(audio, format='audio/mp3')
            
            elif exercise_type == "Sentence building":
                st.write("Arrange the words to form a correct sentence:")
                
                sentences = {
                    "beginner": [
                        {
                            "words": ["I", "to", "school", "go", "every day"],
                            "correct": "I go to school every day."
                        },
                        {
                            "words": ["She", "likes", "ice cream", "chocolate"],
                            "correct": "She likes chocolate ice cream."
                        }
                    ],
                    "intermediate": [
                        {
                            "words": ["Yesterday", "to", "the museum", "went", "they"],
                            "correct": "Yesterday they went to the museum."
                        },
                        {
                            "words": ["have", "studying", "for", "I", "been", "hours"],
                            "correct": "I have been studying for hours."
                        }
                    ],
                    "advanced": [
                        {
                            "words": ["Had", "known", "would", "I", "earlier", "have", "arrived"],
                            "correct": "I would have arrived earlier had I known."
                        },
                        {
                            "words": ["Despite", "difficulties", "the", "succeeded", "they"],
                            "correct": "Despite the difficulties they succeeded."
                        }
                    ]
                }
                
                current_sentences = sentences.get(level, sentences["beginner"])
                selected_sentence = current_sentences[0]  # Just use first one for simplicity
                
                # Display the jumbled words
                st.write(f"Words: {' | '.join(selected_sentence['words'])}")
                
                # Input for user's answer
                user_sentence = st.text_input("Arrange into a sentence:", key="sentence_building")
                
                if st.button("Check Sentence"):
                    # Basic check - could be improved to handle multiple valid arrangements
                    if user_sentence.strip().lower() == selected_sentence['correct'].lower():
                        st.success("Correct! ✅")
                    else:
                        st.error(f"Not quite. A correct answer would be: {selected_sentence['correct']}")
                    
                    # Translate the correct sentence
                    translated = translate_text(selected_sentence['correct'], language_code)
                    st.write(f"Translation: {translated}")
                    
                    # Audio for both English and translated sentence
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("🔊 English:")
                        audio_en = generate_audio(selected_sentence['correct'], 'en')
                        if audio_en:
                            st.audio(audio_en, format='audio/mp3')
                    
                    with col2:
                        st.markdown(f"🔊 {language_choice}:")
                        audio_lang = generate_audio(translated, language_code)
                        if audio_lang:
                            st.audio(audio_lang, format='audio/mp3')
        else:
            st.info("Please select a language to practice grammar.")
    
    # Progress tab
    with tab7:
        if language_code:
            st.header(f"📊 Learning Progress - {language_choice}")
            
            progress_data = get_progress(st.session_state.username, language_code)
            
            if progress_data:
                # Display general statistics
                st.subheader("Your Learning Stats")
                stats = progress_data["stats"]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Words Learned", stats["words_learned"])
                with col2:
                    st.metric("Exercises Completed", stats["exercises_completed"])
                with col3:
                    st.metric("Practice Sessions", stats["practice_sessions"])
                
                # Quiz scores chart
                if "scores" in progress_data and "quiz" in progress_data["scores"] and len(progress_data["scores"]["quiz"]) > 0:
                    st.subheader("Quiz Performance")
                    
                    quiz_scores = progress_data["scores"]["quiz"]
                    scores = [item["score"] for item in quiz_scores]
                    dates = [item["timestamp"] for item in quiz_scores]
                    
                    # Create a pandas DataFrame
                    df = pd.DataFrame({
                        "Date": dates,
                        "Score": scores
                    })
                    
                    # Display the chart
                    st.line_chart(df.set_index("Date"))
                    
                    # Average score
                    avg_score = sum(scores) / len(scores)
                    st.metric("Average Quiz Score", f"{avg_score:.1f}%")
                
                # Recent activity
                st.subheader("Recent Activity")
                activities = progress_data["activities"][-10:]  # Last 10 activities
                
                for activity in reversed(activities):
                    activity_icon = "📚"
                    if activity["activity"] == "vocabulary":
                        activity_icon = "🔤"
                    elif activity["activity"] == "quiz":
                        activity_icon = "🎮"
                    elif activity["activity"] == "practice":
                        activity_icon = "🎯"
                    elif activity["activity"] == "exercise":
                        activity_icon = "✍️"
                    
                    st.write(f"{activity_icon} {activity['activity'].capitalize()} - {activity['timestamp']}")
                
                # Learning suggestions based on activity
                st.subheader("Personalized Learning Suggestions")
                
                # Check what activities user has done less of
                activity_counts = {"vocabulary": 0, "quiz": 0, "practice": 0, "exercise": 0}
                for activity in progress_data["activities"]:
                    act_type = activity["activity"]
                    if act_type in activity_counts:
                        activity_counts[act_type] += 1
                
                # Find least practiced activities
                sorted_activities = sorted(activity_counts.items(), key=lambda x: x[1])
                least_practiced = sorted_activities[0][0]
                
                # Suggestions based on least practiced
                if least_practiced == "vocabulary":
                    st.info("📝 **Suggestion:** Focus on expanding your vocabulary. Try using the Vocabulary section with flashcards to memorize new words.")
                elif least_practiced == "quiz":
                    st.info("🎮 **Suggestion:** Test your knowledge with more quizzes to reinforce what you've learned.")
                elif least_practiced == "practice":
                    st.info("🎯 **Suggestion:** Practice more conversations to improve your fluency and practical language use.")
                elif least_practiced == "exercise":
                    st.info("✍️ **Suggestion:** Work on more grammar exercises to strengthen your understanding of language structure.")
                
                # Progress toward next level
                if level == "beginner":
                    words_needed = 500 - stats["words_learned"]
                    if words_needed > 0:
                        st.progress(stats["words_learned"] / 500)
                        st.write(f"Learn {words_needed} more words to reach intermediate level")
                    else:
                        st.success("Ready to advance to intermediate level!")
                        
                elif level == "intermediate":
                    words_needed = 2000 - stats["words_learned"]
                    if words_needed > 0:
                        st.progress(stats["words_learned"] / 2000)
                        st.write(f"Learn {words_needed} more words to reach advanced level")
                    else:
                        st.success("Ready to advance to advanced level!")
            else:
                st.info("No progress data available yet. Start learning to track your progress!")
                
                # Starting tips
                st.subheader("Getting Started Tips")
                st.markdown("""
                1. Begin with the **Learn** tab to understand basic information about your chosen language
                2. Practice common phrases and basic vocabulary in the **Vocabulary** tab
                3. Take quizzes regularly to test your knowledge
                4. Practice conversations to improve your fluency
                5. Set a regular study schedule - consistency is key!
                """)
        else:
            st.info("Please select a language to view your progress.")
else:
    # Welcome screen when no username is set
    st.title("🌍 Welcome to Language Learner Pro")
    st.write("Your all-in-one tool for learning a new language from basic to intermediate level")
    
