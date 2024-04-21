import sys
from pathlib import Path
import os
from io import BytesIO
 
import requests
import streamlit as st
from PIL import Image
from openai import OpenAI
import os
import streamlit as st
from openai import OpenAI


sys.path.append(str(Path(__file__).resolve().parents[2]))
 

apikey = "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"
 
def main():
    pass
 
if __name__ == '__main__':
    main()

st.title("AI Recipe Generator")
############################################
# OpenAI API setup
############################################

def setup_openai(apikey):
    # Set up OpenAI API key
    os.environ['OPENAI_API_KEY'] = apikey
    OpenAI.api_key = apikey
    client = OpenAI()
    return client
client = setup_openai(apikey)
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

def main():
    pass
############################################
# OpenAI Text Generation
############################################
 
def generate_text_openai_streamlit(client, prompt,text_area_placeholder=None,
                                   model="gpt-3.5-turbo", temperature=0.5,
                                   max_tokens=3000, top_p=1, frequency_penalty=0,
                                   presence_penalty=0, stream=True, html=False):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stream=stream
    )
    complete_response = []
    for chunk in response:
        # Ensure that chunk content is not None before appending
        if chunk.choices[0].delta.content:
            complete_response.append(chunk.choices[0].delta.content)
            result_string = ''.join(complete_response)  # Join without additional spaces
 
            # Auto Scroll
            lines = result_string.count('\n') + 1
            avg_chars_per_line = 80  # Adjust based on expected average line length
            lines += len(result_string) // avg_chars_per_line
            height_per_line = 20  # Adjust as needed
            total_height = lines * height_per_line
 
 
            if text_area_placeholder:
                if html:
                    text_area_placeholder.markdown(result_string, unsafe_allow_html=True)
                else:
                    text_area_placeholder.text_area("Generated Text", value=result_string,height=total_height)
 
    result_string = ''.join(complete_response)
    words = len(result_string.split())  # This is an approximation
    st.text(f"Total Words Generated: {words}")
 
    return result_string

def main():
    pass
 
output_format = ("""
                    <h1> Fun Title of recipe </h1>
                    <h1> Table of Contents</h1> <li> links of content </li>
                    <h1> Introduction </h1><p> dish introduction</p>
                    <h1> Country of Origin </h1><p> Country of Origin</p>
                    <h1> Ingredients </h1><li>Ingredients list </li>
                    <h1> Cooking Steps</h1><li>Cooking Steps list </li>
                    <h1> FAQ </h1><p>question answers</p>
                 """)
 
recipe = st.text_input("Enter your prompt", value="Pasta")
image_prompt = recipe + " realistic, cinematic"
 
if st.button("Create Recipe"):
    with st.spinner('Generating image...'):

        image = generate_image_openai(client, image_prompt)
        st.image(image, caption=recipe, use_column_width=True)
 
    with st.spinner('Generating Recipe...'):
        # Create a placeholder for the text area
        text_area_placeholder = st.markdown("", unsafe_allow_html=True)
 
        prompt = f" Create a detailed cooking recipe for the dish named {recipe}." \
                 f" Include preparation steps and cooking tips." \
                 f" Follow the following format {output_format}"
 
        generate_text_openai_streamlit(client, prompt, text_area_placeholder, html=True)
