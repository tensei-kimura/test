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
Create ONE well-structured multiple choice question for IGCSE Physics Paper 4 on the topic of "Forces". The question must follow this format:

- Clearly written question statement (1-2 lines)
- 4 options labeled A to D
- Only one correct answer
- Provide the correct option letter
- Provide a brief, accurate explanation using IGCSE-level formulas

Make sure the question is realistic and uses correct physics. Do not include unrelated explanations. Use clear and concise English.
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


