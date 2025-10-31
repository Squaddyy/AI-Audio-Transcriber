import streamlit as st
import io

st.set_page_config(layout="wide")
st.title("🎙️ AI Audio Transcriber")

# 1. Add file uploader
uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, etc.)", type=["mp3", "wav", "m4a", "ogg"])

if uploaded_file is not None:
    # Get audio data
    audio_bytes = uploaded_file.read()
    
    # Display audio player
    st.audio(audio_bytes, format=f'audio/{uploaded_file.type.split("/")[-1]}')
    
    st.success("Audio file uploaded successfully.")
    
    # Placeholder for transcription
    st.subheader("Transcription:")
    st.text_area("Your transcript will appear here...", "...", height=200)

else:
    st.info("Please upload an audio file to get started.")