import streamlit as st
import requests

st.title("IGCSE AI Test - Working Model")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
API_KEY = st.secrets["huggingface"]["api_key"]
headers = {"Authorization": f"Bearer {API_KEY}"}

def query(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.json()

prompt = st.text_input("Enter your prompt", "What is the capital of France?")

if st.button("Run"):
    result = query(prompt)
    if isinstance(result, list) and "generated_text" in result[0]:
        st.success("✅ Success!")
        st.write(result[0]["generated_text"])
    else:
        st.error("❌ Unexpected response:")
        st.json(result)
