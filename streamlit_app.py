import streamlit as st
import requests

st.title("IGCSE Science AI Question Generator")

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
API_KEY = st.secrets["huggingface"]["api_key"]
headers = {"Authorization": f"Bearer {API_KEY}"}

def query(prompt):
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except requests.exceptions.JSONDecodeError:
        return {"error": "❌ API did not return valid JSON."}
    except Exception as e:
        return {"error": str(e)}

# ユーザー入力
subject = st.selectbox("Select Subject", ["Physics", "Chemistry", "Biology"])
topic = st.text_input("Topic", "Forces")
question_type = st.selectbox("Question Type", ["Multiple Choice", "Short Answer", "Explanation"])

# プロンプト作成
prompt = f"Create a {question_type} IGCSE {subject} question on the topic '{topic}'. Include the answer and explanation."

# 実行
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

