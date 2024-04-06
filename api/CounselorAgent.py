from langchain.llms import OpenAI
from langchain import HuggingFaceHub
from dotenv import load_dotenv

load_dotenv() # take enviroment variables from .env.


import streamlit as st
import os
## Function to load OpenAI and get responses.

huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
def get_openai_response(question):
    llm = HuggingFaceHub(repo_id="microsoft/phi-1_5",model_kwargs={"temperature":0.5, "max_length":65})
    response=llm(question)
    return response

## initialize our streamlit  app
    
st.set_page_config(page_title="CounselorAgent")

st.header("Welcome to Counselor Agent!")

input = st.text_input("What is your quesiton?", key="input")
response = get_openai_response(input)

submit = st.button("Ask")

## if ask button is clicked

if submit:
    st.subheader("The Response is: ")
    st.write(response)