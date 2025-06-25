import streamlit as st
import requests

st.title("🧪 IGCSE Science Question Generator")

# Hugging Face API settings
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
API_KEY = st.secrets["huggingface"]["api_key"]
headers = {"Authorization": f"Bearer {API_KEY}"}

# API呼び出し関数
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

# 🔹 ユーザー入力インターフェース
subject = st.selectbox("Select Subject", ["Physics", "Chemistry", "Biology"])
topic = st.text_input("Enter Topic (e.g., Forces, Acids and Bases)", "Forces")
question_type = st.selectbox("Select Question Type", ["Multiple Choice", "Short Answer"])

# 🔹 プロンプト生成
if question_type == "Multiple Choice":
    prompt = f"""
    Write ONE IGCSE {subject} Paper 4-style multiple choice question on the topic "{topic}".

    Structure:
    - 1 clearly written question
    - 4 answer choices (A to D)
    - Only one correct answer
    - Clear marking: state the correct letter and give a short explanation using appropriate {subject.lower()} vocabulary
    - The question should assess both recall and application, and be accessible to students at different ability levels.

    Use clear and concise scientific language. Follow IGCSE assessment standards.
    """
else:
    prompt = f"""
    Write ONE IGCSE {subject} Paper 4-style short answer question on the topic "{topic}".

    Structure:
    - A clear question that requires a written response
    - Provide the full correct answer
    - Give a short explanation using appropriate {subject.lower()} vocabulary
    - The question should assess both knowledge and application

    Use clear and concise scientific language. Follow IGCSE assessment standards.
    """

# 🔹 出力セクション
if st.button("Generate Question"):
    result = query(prompt)

    if isinstance(result, list) and "generated_text" in result[0]:
        st.success("✅ Question Generated")
        st.markdown("### 📘 Generated Question:")
        st.markdown(result[0]["generated_text"])
    elif "error" in result:
        st.error(result["error"])
    else:
        st.warning("⚠️ Unexpected output format:")
        st.json(result)
