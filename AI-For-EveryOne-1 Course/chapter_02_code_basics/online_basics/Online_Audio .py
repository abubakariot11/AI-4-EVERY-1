from openai import OpenAI
from apikey import apikey
import os
 
os.environ['OPENAI_API_KEY'] = apikey
OpenAI.api_key = apikey
 
client = OpenAI()
 
audio_file = open("D:\AI Course\chapter 02_code_basics\online_basics\VOICE.mp3", "rb")
 
print("Transcribing audio...")
response = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="text"
)
 
print(response)