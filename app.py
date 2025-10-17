import streamlit as st
import edge_tts
import asyncio

# --- Main App Configuration ---
st.set_page_config(
    page_title="Smart Voice Narrator",
    page_icon="🎙️"
)

st.title("🎙️ Smart Voice Narrator")
st.markdown("Adjust speed, preview, select a voice, and then generate and download your audio.")

# --- UI Elements ---
# These voices support both English and Hindi text input.
VOICE_OPTIONS = {
    "English (Guy - Narrator)": "en-US-GuyNeural",
    "English (Eric)": "en-US-EricNeural",
    "English (Ryan - British)": "en-GB-RyanNeural",
    "English (William - Australian)": "en-AU-WilliamNeural",
    "Hindi (Madhur - Narrator)": "hi-IN-MadhurNeural",
    "Hindi (Swara - Female)": "hi-IN-SwaraNeural"
}

# --- Core Audio Generation Function ---
async def generate_audio(text, voice, rate, output_file):
    """Converts text to speech and saves it."""
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(output_file)
        return True
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False

# --- Speed Adjustment and Preview Section ---
st.markdown("### 1. Adjust Voice Speed & Preview")
col1, col2 = st.columns([3, 1])
with col1:
    rate_percentage = st.slider("Slower <-> Faster", -100, 100, 0, 5)
    rate_str = f"{rate_percentage:+}%"
with col2:
    st.write("")
    st.write("")
    preview_button = st.button("Preview Speed")

# --- Voice Selection and Text Input Section ---
st.markdown("### 2. Choose Voice and Enter Text")
selected_voice_name = st.selectbox("Choose a voice:", options=list(VOICE_OPTIONS.keys()))
VOICE = VOICE_OPTIONS[selected_voice_name]

text_to_convert = st.text_area("Paste your text here (English or Hindi):", height=200, value="This narrator can speak in both English and Hindi. Try it out!")

# --- Main Generate Button ---
st.markdown("### 3. Generate Full Audio")
generate_button = st.button("Generate Audio", type="primary")

# --- LOGIC FOR PREVIEW BUTTON ---
if preview_button:
    sample_text = "This is a preview of the selected speed and voice."
    
    with st.spinner("Generating preview..."):
        if asyncio.run(generate_audio(sample_text, VOICE, rate_str, "preview_output.mp3")):
            st.audio("preview_output.mp3")
            st.success("Preview ready!")

# --- LOGIC FOR MAIN GENERATE BUTTON ---
if generate_button:
    if text_to_convert:
        
        with st.spinner(f"🎙️ Generating audio with the voice of {selected_voice_name}..."):
            output_file_path = "final_narration.mp3"
            success = asyncio.run(generate_audio(text_to_convert, VOICE, rate_str, output_file_path))
            
            if success:
                st.success("✅ Success! Your audio file is ready for playback and download.")
                
                st.audio(output_file_path)

                with open(output_file_path, "rb") as file:
                    st.download_button(
                        label="Download MP3 File",
                        data=file,
                        file_name="narration.mp3",
                        mime="audio/mpeg"
                    )

    else:
        st.warning("Please enter some text to generate the full audio.")

