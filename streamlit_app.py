import streamlit as st
import requests

# --- ページ設定 ---
st.set_page_config(page_title="IGCSE Science Question Generator", layout="centered")

st.title("🧪 IGCSE Science AI Question Generator")

# --- Hugging Face API 設定 ---
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
API_KEY = st.secrets["huggingface"]["api_key"]
headers = {"Authorization": f"Bearer {API_KEY}"}

# --- API 呼び出し関数 ---
def query(prompt):
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- トピック一覧 ---
topics = {
    "Physics": ["Forces", "Energy", "Motion", "Waves"],
    "Chemistry": ["Acids and Bases", "Atomic Structure", "Chemical Reactions"],
    "Biology": ["Enzymes", "Respiration", "Cell Structure"]
}

# --- ユーザー入力 ---
subject = st.selectbox("📚 Select Subject", list(topics.keys()))
topic = st.selectbox("🧪 Select Topic", topics[subject])
question_type = st.radio("📝 Choose Question Type", ["Multiple Choice", "Short Answer"])

# --- プロンプト生成 ---
if question_type == "Multiple Choice":
    prompt = f"""
Write ONE IGCSE {subject} multiple choice question on the topic "{topic}" in the following format:

Question: [Insert the question here]

A) Option A  
B) Option B  
C) Option C  
D) Option D

Answer: [Correct Option Letter]

Explanation: [Short explanation using scientific vocabulary]

The question should assess both recall and application. Use clear and concise scientific language. Follow IGCSE Paper 4 assessment standards.
"""
else:
    prompt = f"""
Write ONE IGCSE {subject} short answer question on the topic "{topic}" in the following format:

Question: [Insert the question here]

Answer: [Insert the full correct answer here]

Explanation: [Short explanation using scientific vocabulary]

The question should assess both recall and application. Use clear and concise scientific language. Follow IGCSE Paper 4 assessment standards.
"""

# --- ボタン実行 ---
if st.button("🚀 Generate Question"):
    result = query(prompt)

    if isinstance(result, list) and "generated_text" in result[0]:
        output = result[0]["generated_text"]

        # --- 出力セクションの分割 ---
        st.success("✅ Question Generated!")

        # Question セクション
        if "Question:" in output:
            question = output.split("Question:")[1].split("Answer:")[0].strip()
            st.markdown("### ❓ **Question**")
            st.markdown(f"{question}")

        # Multiple Choice の選択肢部分（A-D）が含まれているか確認
        if question_type == "Multiple Choice" and any(opt in output for opt in ["A)", "B)", "C)", "D)"]):
            st.markdown("### 🔘 **Choices**")
            choices_part = "\n".join([line for line in output.splitlines() if line.strip().startswith(("A)", "B)", "C)", "D)"))])
            st.markdown(choices_part)

        # Answer
        if "Answer:" in output:
            answer = output.split("Answer:")[1].split("Explanation:")[0].strip()
            st.markdown("### ✅ **Correct Answer**")
            st.markdown(f"**{answer}**")

        # Explanation
        if "Explanation:" in output:
            explanation = output.split("Explanation:")[1].strip()
            st.markdown("### 🧠 **Explanation**")
            st.markdown(explanation)

    elif "error" in result:
        st.error(result["error"])
    else:
        st.warning("⚠️ Unexpected output format")
        st.json(result)




