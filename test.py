import streamlit as st
import os
from google import genai
import google.generativeai as googlegemini

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Gemini 클라이언트 초기화
googlegemini.configure(api_key=GEMINI_API_KEY)

def command_gemini(task, history=None):

    # 대화 히스토리 구성
    history_prompt = ""
    if history:
        for i, (q, a) in enumerate(history):
            history_prompt += f"\nQ{i+1}: {q}\nA{i+1}: {a}\n"

    prompt = f"""
    #below is your current status
    you are excel expert.

    #below is explanation of the person you are talking to
    1. The person is a man
    2. The person is Korean
    3. The person is running a small business
    4. The person is your client

    #These are previous conversations
    {history_prompt}
    #This is the current request
    Q: {task}
    A:

    """

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[prompt]
    )
    return response.text if hasattr(response, "text") else response.candidates[0].content.parts[0].text

# 💬 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # [(질문, 답변), ...]

# Streamlit 앱 UI 구성
st.set_page_config(page_title="Gemini 엑셀 도우미", page_icon="🧠")
st.title("🧠 Gemini 엑셀 도우미 챗봇")
st.write("💬 엑셀 관련 질문을 입력하면 Gemini가 도와줄게요!")

# 사용자 입력 받기
user_input = st.text_area("질문을 입력하세요:", height=150)

if st.button("답변 받기"):
    if user_input.strip() == "":
        st.warning("질문을 입력해주세요!")
    else:
        with st.spinner("답변 생성 중..."):
            # 이전 대화도 함께 전달
            response = command_gemini(user_input, st.session_state.chat_history)

            # 세션 저장
            st.session_state.chat_history.append((user_input, response))

            st.success("답변 완료!")
            st.markdown("### 💡 Gemini의 답변")
            st.write(response)