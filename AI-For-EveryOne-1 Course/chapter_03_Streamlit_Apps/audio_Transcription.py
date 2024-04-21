import os
from io import BytesIO
import streamlit as st
from PIL import Image
import requests
from openai import OpenAI
from apikey import api_key

############################################
# OpenAI API setup
############################################

def setup_openai(api_key):
    # Set up OpenAI API key
    os.environ['OPENAI_API_KEY'] = api_key
    OpenAI.api_key = api_key
    client = OpenAI()
    return client

############################################
# OpenAI Audio to Text
############################################

def generate_text_from_audio_openai(client, audio_file,
                                    model="whisper-1", response_format="text"):
    response = client.audio.transcriptions.create(
        model=model,
        file=audio_file,
        response_format=response_format
    )
    return response

def main_():
    client = setup_openai(api_key)
    st.title("Audio Transcription using OpenAI API")
    audio_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav"])
    
    if audio_file:
        if st.button("Transcribe"):
            st.audio(audio_file, format='audio/wav')
            with st.spinner('Transcribing audio...'):
                try:
                    result = generate_text_from_audio_openai(client, audio_file)
                    print(result)  # Print the result to check if it's empty or contains any error
                    st.write(result)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main_()
