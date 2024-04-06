import requests
import streamlit as st

def get_counsel_response(input_topic):
    response = requests.post("http://localhost:8000/counsel", json={'topic': input_topic})
    if response.status_code == 200:
        return response.json()['response']
    else:
        return "Error: Could not retrieve the response."

st.title("Counselor Agent Interface")
input_topic = st.text_input("How can I assist you today?")

if input_topic:
    response = get_counsel_response(input_topic)
    st.write(response)
