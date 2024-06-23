import streamlit as st

with st.sidebar:
    ngrok_url = st.text_input("Ngrok URL", key="ngrok_url")

st.title("💬 당신 삶의 북극성은 무엇인가요?:star:")
st.caption("🚀 북극성 찾기!!")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "당신의 꿈은 무엇일까요?"}]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # if not ngrok_url:
    #     st.info("Please add your ngrok_url to continue.")
    #     st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 호출 및 전처리
    response = "오라마 응답 부분"
    msg = response

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
