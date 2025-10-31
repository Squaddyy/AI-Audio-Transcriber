import streamlit as st
import io
import librosa
from transformers import pipeline
import base64 

st.set_page_config(layout="wide")

# --- CSS Styling ---

def load_css(file_name):
    """Loads a local CSS file."""
    try:
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}")

# Load custom CSS
load_css("assets/style.css")

# --- AI Model Loading ---

@st.cache_resource
def load_transcription_model():
    """
    Loads and caches the Whisper ASR model.
    Using 'base' for a balance of speed and multilingual accuracy.
    """
    st.info("Loading transcription model... This may take a moment on first run.")
    try:
        transcriber = pipeline(
            "automatic-speech-recognition", 
            model="openai/whisper-base"
        )
        st.success("Multilingual transcription model loaded successfully!")
        return transcriber
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Load the model
transcriber = load_transcription_model()

# --- Application UI ---

st.title("🎙️ AI Audio Transcriber")
st.text("Upload your audio file and our AI will transcribe it into text.")

if transcriber is None:
    st.error("Model failed to load. Please check logs or restart the app.")
else:
    # Main layout with two columns
    col1, col2 = st.columns(2)

    # --- Column 1: Uploads & Audio Player ---
    with col1:
        st.header("1. Upload Audio")
        
        uploaded_file = st.file_uploader(
            "Upload an audio file (MP3, WAV, M4A, OGG)", 
            type=["mp3", "wav", "m4a", "ogg"],
            label_visibility="collapsed"
        )
        
        audio = None  # Initialize audio variable

        if uploaded_file is not None:
            audio_bytes = uploaded_file.read()
            st.audio(audio_bytes, format=f'audio/{uploaded_file.type.split("/")[-1]}')
            
            st.info("Pre-processing audio for transcription...")
            try:
                # Pre-process audio: load and resample to 16kHz for Whisper
                audio_file_like = io.BytesIO(audio_bytes)
                audio, sample_rate = librosa.load(audio_file_like, sr=16000)
                st.success("Audio pre-processing complete.")
            except Exception as e:
                st.error(f"Error processing audio file: {e}")
                audio = None
        else:
            st.info("Please upload an audio file to get started.")

    # --- Column 2: Transcription Output ---
    with col2:
        st.header("2. Get Transcription")
        
        if audio is not None:
            # Display transcribe button only if audio is processed
            if st.button("Transcribe Audio", type="primary", use_container_width=True):
                try:
                    with st.spinner("Transcribing... This may take a moment."):
                        # Perform transcription
                        result = transcriber(audio, return_timestamps=True)
                        transcription_text = result["text"].strip()

                    # Display the transcription
                    st.text_area("Transcript:", transcription_text, height=300)
                    st.success("Transcription complete!")
                    
                except Exception as e:
                    st.error(f"An error occurred during transcription: {e}")
        else:
            st.warning("Please upload and process an audio file first.")