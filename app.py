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
st.markdown("Adjust the voice speed, preview it, select a voice, and then generate your full audio.")

# --- UI Elements ---
VOICE_OPTIONS = {
    "English (Guy - Narrator)": "en-US-GuyNeural",
    "English (Eric)": "en-US-EricNeural",
    "English (Ryan - British)": "en-GB-RyanNeural",
    "English (William - Australian)": "en-AU-WilliamNeural",
    "Hindi (Madhur - Narrator)": "hi-IN-MadhurNeural"
}

# --- Core Audio Generation Function ---
# This function is used by both the preview and the main generation
async def generate_audio(text, voice, rate, output_file):
    """Converts text to speech using edge-tts with a specified rate and saves it."""
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(output_file)
        return True
    except Exception as e:
        if "No audio was received" in str(e):
             st.error("Error: The selected voice may not support the language of the text.")
        else:
            st.error(f"An error occurred: {e}")
        return False

# --- Speed Adjustment and Preview Section ---
st.markdown("### 1. Adjust Voice Speed & Preview")

# Use columns for a cleaner layout
col1, col2 = st.columns([3, 1])

with col1:
    rate_percentage = st.slider(
        "Slower <-> Faster",
        -100, 100, 0, 5
    )
    rate_str = f"{rate_percentage:+}%" # Format for edge-tts (e.g., "+20%")

with col2:
    # This empty space is for vertical alignment of the button
    st.write("") 
    st.write("")
    preview_button = st.button("Preview Speed")

# --- Voice Selection and Text Input Section ---
st.markdown("### 2. Choose Voice and Enter Text")
selected_voice_name = st.selectbox(
    "Choose a default voice:",
    options=list(VOICE_OPTIONS.keys())
)
VOICE = VOICE_OPTIONS[selected_voice_name]

text_to_convert = st.text_area(
    "Paste your text here (English or Hindi):",
    height=200,
    value="You can test different speeds with the preview button before generating the final audio."
)

# --- Main Generate Button ---
st.markdown("### 3. Generate Full Audio")
generate_button = st.button("Generate Audio", type="primary")


# --- LOGIC FOR PREVIEW BUTTON ---
if preview_button:
    # Determine the correct sample text based on the selected voice
    sample_text = "This is a preview of the selected speed and voice."
    if "Hindi" in selected_voice_name:
        sample_text = "यह चुनी हुई गति और आवाज़ का पूर्वावलोकन है।"
    
    with st.spinner("Generating preview..."):
        success = asyncio.run(generate_audio(sample_text, VOICE, rate_str, "preview_output.mp3"))
        if success:
            st.audio("preview_output.mp3", format='audio/mp3')
            st.success("Preview generated successfully!")
        # Error is handled inside generate_audio

# --- LOGIC FOR MAIN GENERATE BUTTON ---
if generate_button:
    if text_to_convert:
        final_voice = VOICE
        final_voice_name = selected_voice_name

        try:
            detected_lang = detect(text_to_convert)
            if detected_lang == 'hi':
                st.info("🇮🇳 Hindi text detected! Automatically switching to the Hindi narrator.")
                final_voice = "hi-IN-MadhurNeural"
                final_voice_name = "Hindi (Madhur - Narrator)"
        except LangDetectException:
            st.warning("Could not detect language, using the selected voice.")

        with st.spinner(f"🎙️ Generating audio with the voice of {final_voice_name}..."):
            success = asyncio.run(generate_audio(text_to_convert, final_voice, rate_str, "character_voice_output.mp3"))
            
            if success:
                st.success("✅ Success! Your full audio file is ready.")
                st.audio("character_voice_output.mp3", format='audio/mp3')
    else:
        st.warning("Please enter some text to generate the full audio.")
