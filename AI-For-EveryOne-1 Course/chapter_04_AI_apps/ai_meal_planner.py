import os
import streamlit as st
import openai
import json
import sys
from pathlib import Path
from openai import OpenAI
from openai import OpenAI
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[2]))

def setup_openai(apikey):
    # Set up OpenAI API key
    os.environ['OPENAI_API_KEY'] = apikey
    OpenAI.api_key = apikey
    client = OpenAI()
    return client
client = setup_openai("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")
############################################
# OpenAI Text Generation
############################################
 
def generate_text_openai_streamlit(prompt ,text_area_placeholder=None,
                                   model="gpt-3.5-turbo", temperature=0.5,
                                   max_tokens=3000, top_p=1, frequency_penalty=0,
                                   presence_penalty=0, stream=True, html=False):
    complete_response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stream=stream
    )

    if text_area_placeholder:
        text_area_placeholder.text_area("Generated Text", value=complete_response)

    words = len(complete_response.split())  # This is an approximation
    st.text(f"Total Words Generated: {words}")

    return complete_response

def main():
    pass

if __name__ == '__main__':
    apikey = "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"  # Replace "YOUR_API_KEY" with your actual API key
    setup_openai(apikey)
    main()

st.title("AI Meal Planner")

# Create columns for inputs
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox('Gender', ('Male', 'Female', 'Other'), key='gender_selectbox')
    weight = st.number_input('Weight (kg):', min_value=30, value=80, key='weight_input')
with col2:
    age = st.number_input('Age', min_value=18, max_value=120, step=1, value=30, key='age_input')
    height = st.number_input('Height (cm)', min_value=1, max_value=250, step=1, value=170, key='height_input')

aim = st.selectbox('Aim', ('Lose', 'Gain', 'Maintain'), key='aim_selectbox')

user_data = f""" - I am a {gender}"
                - My weight is {weight} kg"
                - I am {age} years old"
                - My height is {height} cm"
                - My aim is to {aim} weight
             """
output_format = """ "range":"Range of ideal weight",
                    "target":"Target weight",
                    "difference":"Weight i need to lose or gain",
                    "bmi":"my BMI",
                    "meal_plan":"Meal plan for 7 days",
                    "total_days":"Total days to reach target weight",
                    "weight_per_week":"Weight to lose or gain per week",
                                    """

prompt = user_data + (" given the information, follow the output format as follows."
                      " Give only JSON format nothing else ") + output_format

if st.button("Generate Meal Plan"):
    with st.spinner('Creating Meal plan'):
        text_area_placeholder = st.empty()
        meal_plan = generate_text_openai_streamlit(prompt, model="gpt-3.5-turbo",
                                                   text_area_placeholder=text_area_placeholder)
        meal_plan_json = json.loads(meal_plan)

        st.title("Meal Plan")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Range")
            st.write(meal_plan_json["range"])
            st.subheader("Target")
            st.write(meal_plan_json["target"])
        with col2:
            st.subheader("BMI")
            st.write(meal_plan_json["bmi"])
            st.subheader("Days")
            st.write(meal_plan_json["total_days"])

        with col3:
            st.subheader(f"{aim}")
            st.write(meal_plan_json["difference"])
            st.subheader("Per week")
            st.write(meal_plan_json["weight_per_week"])

        st.subheader("Meal plan for 7 days")
        st.write(meal_plan_json["meal_plan"])
