import streamlit as st
import requests

st.set_page_config(page_title="IGCSE Science Question Generator", layout="centered")

st.title("🧪 IGCSE Science AI Question Generator")

# Hugging Face API 設定
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
API_KEY = st.secrets["huggingface"]["api_key"]
headers = {"Authorization": f"Bearer {API_KEY}"}

# API 呼び出し関数
def query(prompt):
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# トピック一覧
topics = {
    "Physics": ["Forces", "Energy", "Motion", "Waves"],
    "Chemistry": ["Acids and Bases", "Atomic Structure", "Chemical Reactions"],
    "Biology": ["Enzymes", "Respiration", "Cell Structure"]
}

# UI: 教科・トピック・タイプ選択
subject = st.selectbox("📚 Select Subject", list(topics.keys()))
topic = st.selectbox("🧪 Select Topic", topics[subject])
question_type = st.radio("📌 Choose Question Type", ["Multiple Choice", "Short Answer"])

# プロンプト生成
if question_type == "Multiple Choice":
    prompt = f"""
Write ONE IGCSE {subject} Paper 4-style multiple choice question on the topic "{topic}".

Structure:
- Start with the word "Question:" followed by the actual question.
- Then list 4 answer choices (A to D) clearly.
- Clearly state the correct answer below with "Answer: [Letter]".
- Below that, give a short explanation using appropriate {subject.lower()} vocabulary under the heading "Explanation:".

Use clear and concise scientific language. Follow IGCSE assessment standards. Assess both recall and application.
"""
else:
    prompt = f"""
Write ONE IGCSE {subject} Paper 4-style short answer question on the topic "{topic}".

Structure:
- Start with the word "Question:" followed by the actual question.
- Then write "Answer:" followed by the full correct answer.
- Below that, give a short explanation using appropriate {subject.lower()} vocabulary under the heading "Explanation:".

Use clear and concise scientific language. Follow IGCSE assessment standards. Assess both recall and application.
"""

# ボタンで実行
if st.button("🚀 Generate Question"):
    result = query(prompt)

    if isinstance(result, list) and "generated_text" in result[0]:
        output = result[0]["generated_text"]

        # 分割して表示
        st.success("✅ Question Generated!")

        if "Question:" in output:
            question = output.split("Question:")[1].split("A)")[0].strip()
            st.markdown("### ❓ **Question**")
            st.markdown(f"{question}")

        if "A)" in output:
            choices_raw = output.split("A)")[1].split("Answer:")[0].strip()
            choices = choices_raw.replace("B)", "\n\n**B)**").replace("C)", "\n\n**C)**").replace("D)", "\n\n**D)**")
            st.markdown("### 🔘 **Choices**")
            st.markdown("**A)** " + choices)

        if "Answer:" in output:
            answer = output.split("Answer:")[1].split("Explanation:")[0].strip()
            st.markdown("### ✅ **Correct Answer**")
            st.markdown(f"**{answer}**")

        if "Explanation:" in output:
            explanation = output.split("Explanation:")[1].strip()
            st.markdown("### 🧠 **Explanation**")
            st.markdown(f"{explanation}")

    elif "error" in result:
        st.error(result["error"])
    else:
        st.warning("⚠️ Unexpected output format")
        st.json(result)



