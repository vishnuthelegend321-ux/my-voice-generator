import streamlit as st
import edge_tts
import asyncio
from langdetect import detect, LangDetectException

# --- Main App Configuration ---
st.set_page_config(
    page_title="Smart Voice Narrator",
    page_icon="🎙️"
)

st.title("🎙️ Smart Voice Narrator")
st.markdown("This app automatically detects Hindi text and switches to the appropriate voice.")

# --- UI Elements ---
VOICE_OPTIONS = {
    "English (Guy - Narrator)": "en-US-GuyNeural",
    "English (Eric)": "en-US-EricNeural",
    "English (Ryan - British)": "en-GB-RyanNeural",
    "English (William - Australian)": "en-AU-WilliamNeural",
    "Hindi (Madhur - Narrator)": "hi-IN-MadhurNeural"
}

selected_voice_name = st.selectbox(
    "Choose a default voice:",
    options=list(VOICE_OPTIONS.keys())
)
# Get the user's default choice
VOICE = VOICE_OPTIONS[selected_voice_name]

text_to_convert = st.text_area(
    "Paste your text here (English or Hindi):",
    height=200,
    value="Hello world! Or paste Hindi text like: नमस्ते दुनिया!"
)

generate_button = st.button("Generate Audio", type="primary")

# --- Core Logic ---
OUTPUT_FILE = "character_voice_output.mp3"

async def generate_audio(text, voice, output_file):
    """Converts text to speech using edge-tts and saves it."""
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        return True, output_file
    except Exception as e:
        # Catch the specific "No audio was received" error
        if "No audio was received" in str(e):
             st.error("Error: The selected voice may not support the language of the text. Please check your input.")
        else:
            st.error(f"An error occurred: {e}")
        return False, str(e)

# This block runs when the "Generate Audio" button is clicked
if generate_button:
    if text_to_convert:
        # Set default voices
        final_voice = VOICE
        final_voice_name = selected_voice_name

        # --- Language Detection Logic ---
        try:
            # Detect the language of the input text
            detected_lang = detect(text_to_convert)
            
            # If Hindi is detected, override the user's choice
            if detected_lang == 'hi':
                st.info("🇮🇳 Hindi text detected! Automatically switching to the Hindi narrator.")
                final_voice = "hi-IN-MadhurNeural"
                final_voice_name = "Hindi (Madhur - Narrator)"

        except LangDetectException:
            # If detection fails (e.g., text is too short), just use the selected voice
            st.warning("Could not detect language, using the selected voice.")
        
        # --- End of Language Detection Logic ---

        with st.spinner(f"🎙️ Generating audio with the voice of {final_voice_name}..."):
            # Use the final_voice, which may have been changed by the detector
            success, result = asyncio.run(generate_audio(text_to_convert, final_voice, OUTPUT_FILE))
            
            if success:
                st.success("✅ Success! Your audio file is ready.")
                st.audio(OUTPUT_FILE, format='audio/mp3')
    else:
        st.warning("Please enter some text to generate audio.")
