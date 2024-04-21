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

# Call the main_() function to start the Streamlit app
                    

############################################
# OpenAI Image Generation
############################################
def generate_image_openai(client, prompt, model="dall-e-2", size="1024x1024", n=1):
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        n=n,
    )
    image_url = response.data[0].url
    image = requests.get(image_url)
    image = Image.open(BytesIO(image.content))
    return image

def main_():
    #### Image Generation ####
    client = setup_openai(api_key)
    st.title("Image Generation using OpenAI API")
    prompt = st.text_input("Enter your prompt", value="A cute cat jumping over a fence, cartoon, colorful")
    if st.button("Generate Image"):
        with st.spinner('Generating image...'):
            image = generate_image_openai(client, prompt)
            st.image(image)
            



if __name__ == "__main__":
    main_()
