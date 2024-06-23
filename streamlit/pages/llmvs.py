import streamlit as st
from langchain_community.chat_models import ChatOllama

gemma = 'gemma:7b-instruct'
llama = 'llama3:8b'

def get_response(model, prompt, url):
    model_gemma = ChatOllama(
        model=model, temperature=0, base_url=url, verbose=True
    )
    return model_gemma.stream(prompt)


with st.sidebar:
    ollama_ngrok_url = st.text_input("Ollama Ngrok URL", key="ollama_ngrok_url")


st.title("💬 당신 삶의 북극성은 무엇인가요?:star:")
st.caption("🚀 북극성 찾기!!")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "당신의 꿈은 무엇일까요?"}]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not ollama_ngrok_url:
        st.info("Please add your ngrok_url to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 호출 및 전처리
    with st.chat_message(gemma):
        with st.spinner("대답 중 ..."):
            response = st.write_stream(get_response(model=gemma, prompt=prompt, url=ollama_ngrok_url))
    st.session_state.messages.append({"role": gemma, "content": response})

    with st.chat_message(llama):
        with st.spinner("대답 중 ..."):
            response = st.write_stream(get_response(model=llama, prompt=prompt, url=ollama_ngrok_url))
    st.session_state.messages.append({"role": llama, "content": response})

