import streamlit as st
import edge_tts
import asyncio

# --- Main App Configuration ---
st.set_page_config(
    page_title="Multi-Character Voice Narrator",
    page_icon="🎙️"
)

st.title("🎙️ Multi-Character Voice Narrator")
st.markdown("Select a voice, enter your text, and click 'Generate Audio' to create your narration.")

# --- UI Elements ---
VOICE_OPTIONS = {
    "English (Guy - Narrator)": "en-US-GuyNeural",
    "English (Eric)": "en-US-EricNeural",
    "English (Ryan - British)": "en-GB-RyanNeural",
    "English (William - Australian)": "en-AU-WilliamNeural",
    "Hindi (Madhur - Narrator)": "hi-IN-MadhurNeural"
}

selected_voice_name = st.selectbox(
    "Choose your character voice:",
    options=list(VOICE_OPTIONS.keys())
)
VOICE = VOICE_OPTIONS[selected_voice_name]

text_to_convert = st.text_area(
    "Paste your text here:",
    height=200,
    value="Hello world! This is a demonstration of a text-to-speech web application."
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
        st.error(f"An error occurred: {e}")
        return False, str(e)

if generate_button:
    if text_to_convert:
        with st.spinner(f"🎙️ Generating audio with the voice of {selected_voice_name}..."):
            success, result = asyncio.run(generate_audio(text_to_convert, VOICE, OUTPUT_FILE))

            if success:
                st.success("✅ Success! Your audio file is ready.")
                st.audio(OUTPUT_FILE, format='audio/mp3')
    else:
        st.warning("Please enter some text to generate audio.")
