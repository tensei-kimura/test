import streamlit as st
import requests
import urllib.parse

# -------------------------------
# Personal Branding
# -------------------------------
st.set_page_config(page_title="IGCSE AI Question Generator", page_icon="🧪")
st.image("https://your-logo-link-here.png", width=100)  # ← 自分のロゴ画像URL
st.title("🧪 IGCSE Science Question Generator")
st.caption("by Your Name")  # ← 自分の名前に置き換え

# Hugging Face API設定
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
API_KEY = st.secrets["huggingface"]["api_key"]
headers = {"Authorization": f"Bearer {API_KEY}"}

# API呼び出し
def query(prompt):
    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": 0.9,  # 多様性を高める
                "top_p": 0.95,
                "max_new_tokens": 1200  # 10問まとめて出すので多め
            }
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# トピック辞書（拡張版）
topics = {
    "Physics": ["Forces", "Energy", "Motion", "Waves", "Electricity", "Magnetism", "Thermal Physics"],
    "Chemistry": ["Acids and Bases", "Atomic Structure", "Chemical Reactions", "Periodic Table", "Organic Chemistry", "Electrolysis"],
    "Biology": ["Enzymes", "Respiration", "Cell Structure", "Digestion", "Genetics", "Ecology", "Human Circulatory System"]
}

# UI選択項目
subject = st.selectbox("Select Subject", list(topics.keys()))
topic = st.selectbox("Select Topic", topics[subject])
question_type = st.radio("Choose Question Type", ["Multiple Choice", "Short Answer"])

# プロンプト生成（10問まとめて）
if question_type == "Multiple Choice":
    prompt = f"""
Write 10 UNIQUE IGCSE {subject} Paper 4-style multiple choice questions on the topic "{topic}".
Each question must follow this structure:

Question X:
- The question text
- Options A-D
- Answer: [Correct Letter]
- Explanation: [short explanation]

Make sure all 10 questions are different, covering recall, understanding, and application.
"""
else:
    prompt = f"""
Write 10 UNIQUE IGCSE {subject} Paper 4-style short answer questions on the topic "{topic}".
Each question must follow this structure:

Question X:
- The question text
- Answer: [Correct Answer]
- Explanation: [short explanation]

Make sure all 10 questions are different, covering recall, understanding, and application.
"""

# 履歴保持
if "questions" not in st.session_state:
    st.session_state["questions"] = []

# 実行と表示
if st.button("Generate 10 Questions"):
    result = query(prompt)

    if isinstance(result, list) and "generated_text" in result[0]:
        output = result[0]["generated_text"]
        st.session_state["questions"].append(output)
    elif "error" in result:
        st.error(result["error"])

# 保存したすべての問題を表示
for set_idx, output in enumerate(st.session_state["questions"], 1):
    st.markdown(f"# 📚 Question Set {set_idx}")

    # 各問題ごとに分割
    questions = output.split("Question")
    for q in questions:
        if not q.strip():
            continue
        st.markdown(f"## ❓ Question{q[:3].strip()}")

        # Question部分
        if "Answer:" in q:
            q_text = q.split("Answer:")[0].strip()
            st.markdown(q_text)

        # Answer部分
        if "Answer:" in q:
            ans = q.split("Answer:")[1].split("Explanation:")[0].strip()
            st.markdown(f"**✅ Answer:** {ans}")

        # Explanation部分
        if "Explanation:" in q:
            exp = q.split("Explanation:")[1].strip()
            st.markdown(f"**🧠 Explanation:** {exp}")

        # Research用リンク
        query_url = urllib.parse.quote(f"{topic} IGCSE {subject}")
        st.markdown(f"[🔗 Research More]("
                    f"https://www.google.com/search?q={query_url})")

        st.markdown("---")

    else:
        st.warning("⚠️ Unexpected output:")
        st.json(result)
