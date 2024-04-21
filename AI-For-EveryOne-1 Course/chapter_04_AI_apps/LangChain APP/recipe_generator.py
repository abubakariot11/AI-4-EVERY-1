from dotenv import load_dotenv
import os
import streamlit as st
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


load_dotenv()

API_KEY = os.environ['OPENAI_API_KEY']

llm = OpenAI(openai_api_key=API_KEY, temperature=0.9)

prompt_template = PromptTemplate(
    template="Give an example of a meal could be made using the following ingredients:{ingredients}",
    input_variables = ['ingredients']

)

meal_chain = LLMChain(
    llm = llm,
    prompt = prompt_template,
    verbose = True

)


st.title("AI Recipe Generator")
user_prompt = st.text_input("Enter a comma-separated list of ingredients:")

if st.button("Generate Recipe") and user_prompt:
    with st.spinner("Generating Recipe..."):
        output = meal_chain.run(ingredients=user_prompt)
        st.write(output)

