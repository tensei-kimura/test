import streamlit as st
import requests

st.title("IGCSE AI Test - Working Model")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
API_KEY = st.secrets["huggingface"]["api_key"]
headers = {"Authorization": f"Bearer {API_KEY}"}

def query(prompt):
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()  # HTTPエラーがあれば例外にする
        return response.json()       # JSONで正しく返ってくる場合
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except requests.exceptions.JSONDecodeError:
        return {"error": "❌ API did not return valid JSON (e.g., model not available, or token invalid)."}
    except Exception as e:
        return {"error": str(e)}


prompt = st.text_input("Enter your prompt", "What is the capital of France?")

if st.button("Run"):
    result = query(prompt)

    if isinstance(result, list) and "generated_text" in result[0]:
        st.success("✅ Success!")
        st.write(result[0]["generated_text"])
    elif "error" in result:
        st.error(result["error"])
    else:
        st.warning("⚠️ Unexpected output format:")
        st.json(result)
