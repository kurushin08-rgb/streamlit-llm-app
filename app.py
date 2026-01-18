from dotenv import load_dotenv

load_dotenv()

import streamlit as st
st.title("サンプルアプリ: 専門選択型LLM Webアプリ")

# =========================
# アプリ概要・操作説明
# =========================
st.write("### アプリ概要")
st.write(
    """
    本アプリでは、ラジオボタンで **LLMに振る舞わせる専門家の種類** を選択できます。  
    選択した専門家に応じて、LLMへ渡す **システムメッセージ（役割定義）** が切り替わります。
    """
)

st.write("### 操作方法")
st.write(
    """
    1. 専門家の種類をラジオボタンで選択してください  
    2. 入力フォームに質問・相談内容を入力してください  
    3. 「実行」ボタンを押すと、選択した専門家の視点で回答が表示されます  
    """
)

st.divider()

# =========================
# 専門家選択
# =========================
selected_expert = st.radio(
    "専門家の種類を選択してください。",
    ["A: システムエンジニア", "B: マーケティングコンサルタント", "C: データサイエンティスト"]
)

st.divider()

# =========================
# 入力フォーム
# =========================
input_text = st.text_input(
    label="LLMに質問したい内容を入力してください。"
)

# =========================
# 専門家ごとの system メッセージ
# =========================
def get_system_message(expert_type):
    if expert_type.startswith("A"):
        return (
            "あなたは経験豊富なシステムエンジニアです。"
            "要件定義、設計、実装、運用の観点から、"
            "技術的に正確で実務に役立つ回答をしてください。"
        )
    elif expert_type.startswith("B"):
        return (
            "あなたは優秀なマーケティングコンサルタントです。"
            "市場分析、顧客視点、KPI、施策立案の観点から、"
            "ビジネス的に分かりやすい回答をしてください。"
        )
    else:
        return (
            "あなたはデータサイエンティストです。"
            "統計、データ分析、機械学習の観点から、"
            "根拠を重視して論理的に回答してください。"
        )

 

# =========================
# LLM呼び出し関数
# =========================
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

def ask_llm(input_text, expert_type):
    system_message = get_system_message(expert_type)

    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0
    )

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text),
    ]

    result = llm(messages)

    return result.content

# =========================
# 実行ボタン
# =========================
if st.button("実行"):
    st.divider()

    if input_text:
        try:
            answer = ask_llm(input_text, selected_expert)
            st.write("### LLMからの回答")
            st.write(answer)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

    else:
        st.error("質問内容を入力してから「実行」ボタンを押してください。")