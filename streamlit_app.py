import streamlit as st
import requests

st.title("IGCSE Physics Question Generator - Forces (Paper 4 Style)")

# Hugging Face API settings
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
API_KEY = st.secrets["huggingface"]["api_key"]
headers = {"Authorization": f"Bearer {API_KEY}"}

# 安全なリクエスト送信関数
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

# プロンプトの自動生成
prompt = """
Write ONE IGCSE Physics Paper 4-style multiple choice question on the topic "Forces".

Structure:
- 1 clearly written question
- 4 answer choices (A to D)
- Only one correct answer
- Clear marking: state the correct letter and give a short explanation using appropriate physics vocabulary
- The question should assess both recall and application, and be accessible to students at different ability levels.

Use clear and concise scientific language. Follow IGCSE assessment standards.
"""


st.code(prompt.strip(), language="markdown")

if st.button("Generate Question"):
    result = query(prompt)

    if isinstance(result, list) and "generated_text" in result[0]:
        st.success("✅ Question Generated Successfully!")
        st.markdown("### 🧠 IGCSE Question Output")
        st.markdown(result[0]["generated_text"])
    elif "error" in result:
        st.error(result["error"])
    else:
        st.warning("⚠️ Unexpected output format:")
        st.json(result)


