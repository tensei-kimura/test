import streamlit as st
import requests

st.title("🧪 IGCSE Science Question Generator")

# Hugging Face API設定
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"
API_KEY = st.secrets["huggingface"]["api_key"]
headers = {"Authorization": f"Bearer {API_KEY}"}

# API呼び出し
def query(prompt):
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# トピック辞書
topics = {
    "Physics": ["Forces", "Energy", "Motion", "Waves"],
    "Chemistry": ["Acids and Bases", "Atomic Structure", "Chemical Reactions"],
    "Biology": ["Enzymes", "Respiration", "Cell Structure"]
}

# UI選択項目
subject = st.selectbox("Select Subject", list(topics.keys()))
topic = st.selectbox("Select Topic", topics[subject])
question_type = st.radio("Choose Question Type", ["Multiple Choice", "Short Answer"])

# プロンプト生成
if question_type == "Multiple Choice":
    prompt = f"""
Write ONE IGCSE {subject} Paper 4-style multiple choice question on the topic "{topic}".

Structure:

- Start with the word "Question:" followed by the actual question.
- Then list 4 answer choices (A to D) clearly.
- Clearly state the correct answer below with "Answer: [Letter]".
- Below that, give a short explanation using appropriate {subject.lower()} vocabulary under the heading "Explanation:".

The question should assess both recall and application, and be accessible to students at different ability levels.
Use clear and concise scientific language. Follow IGCSE assessment standards.
"""
else:
    prompt = f"""
Write ONE IGCSE {subject} Paper 4-style short answer question on the topic "{topic}".

Structure:

- Start with the word "Question:" followed by the actual question.
- Then write "Answer:" followed by the full correct answer.
- Below that, give a short explanation using appropriate {subject.lower()} vocabulary under the heading "Explanation:".

The question should assess both recall and application, and be accessible to students at different ability levels.
Use clear and concise scientific language. Follow IGCSE assessment standards.
"""

# 実行と表示
if st.button("Generate Question"):
    result = query(prompt)

    if isinstance(result, list) and "generated_text" in result[0]:
        output = result[0]["generated_text"]

        # ラベルごとに分けて表示
        st.success("✅ Question Generated!")

        if "Question:" in output:
            st.markdown("### ❓ Question")
            question_part = output.split("Question:")[1].split("A)")[0].strip()
            st.markdown(question_part)

        if "A)" in output:
            st.markdown("### 🔘 Choices")
            choices = output.split("A)")[1].split("Answer:")[0].strip()
            st.markdown("A) " + choices.replace("B)", "\n\nB)").replace("C)", "\n\nC)").replace("D)", "\n\nD)"))

        if "Answer:" in output:
            st.markdown("### ✅ Answer")
            answer = output.split("Answer:")[1].split("Explanation:")[0].strip()
            st.markdown(answer)

        if "Explanation:" in output:
            st.markdown("### 🧠 Explanation")
            explanation = output.split("Explanation:")[1].strip()
            st.markdown(explanation)

    elif "error" in result:
        st.error(result["error"])
    else:
        st.warning("⚠️ Unexpected output:")
        st.json(result)
