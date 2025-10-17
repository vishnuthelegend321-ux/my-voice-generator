import streamlit as st
from gtts import gTTS
from langdetect import detect, LangDetectException
import os

# --- Main App Configuration ---
st.set_page_config(
    page_title="Smart Voice Narrator",
    page_icon="🎙️"
)

st.title("🎙️ Smart Voice Narrator")
st.markdown("Select a language, enter your text, and then generate and download your audio.")

# --- UI Elements (Updated for gTTS) ---
# gTTS uses language codes, not specific voice names.
VOICE_OPTIONS = {
    "English": "en",
    "Hindi": "hi"
}

# --- Core Audio Generation Function (Updated for gTTS) ---
def generate_audio(text, lang, output_file):
    """Converts text to speech using gTTS and saves it."""
    try:
        # Create a gTTS object.
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)
        return True
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False

# --- Voice Selection and Text Input Section ---
st.markdown("### 1. Choose Language and Enter Text")
selected_language_name = st.selectbox("Choose a default language:", options=list(VOICE_OPTIONS.keys()))
LANGUAGE_CODE = VOICE_OPTIONS[selected_language_name]

text_to_convert = st.text_area("Paste your text here (English or Hindi):", height=200, value="Hello! You can now generate audio using Google's Text-to-Speech service.")

# --- Main Generate Button ---
st.markdown("### 2. Generate Full Audio")
generate_button = st.button("Generate Audio", type="primary")

# --- LOGIC FOR MAIN GENERATE BUTTON ---
if generate_button:
    if text_to_convert:
        final_lang_code = LANGUAGE_CODE
        final_lang_name = selected_language_name

        # --- Automatic Language Detection ---
        try:
            detected_lang = detect(text_to_convert)
            if detected_lang == 'hi':
                st.info("🇮🇳 Hindi text detected! Switching to the Hindi voice.")
                final_lang_code, final_lang_name = "hi", "Hindi"
            elif detected_lang == 'en':
                final_lang_code, final_lang_name = "en", "English"
        except LangDetectException:
            st.warning("Could not automatically detect language, using the selected default.")

        with st.spinner(f"🎙️ Generating audio in {final_lang_name}..."):
            output_file_path = "final_narration.mp3"
            success = generate_audio(text_to_convert, final_lang_code, output_file_path)
            
            if success:
                st.success("✅ Success! Your audio file is ready for playback and download.")
                
                # Embed the audio player for listening
                st.audio(output_file_path)

                # --- Download Button Logic ---
                with open(output_file_path, "rb") as file:
                    st.download_button(
                        label="Download MP3 File",
                        data=file,
                        file_name="narration.mp3",
                        mime="audio/mpeg"
                    )
    else:
        st.warning("Please enter some text to generate the audio.")

