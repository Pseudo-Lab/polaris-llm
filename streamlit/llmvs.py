import streamlit as st
import requests
import json
from langchain_community.chat_models import ChatOllama

gemma = 'gemma:7b-instruct'
llama = 'llama3:8b'
finetuned = 'bcmin1018/gemma-7b-persona-pessimistic:latest'

def response_component(model, prompt):
    with st.chat_message(model):
        with st.spinner("대답 중 ..."):
            response = st.write_stream(get_response(model=model, prompt=prompt, url=ollama_ngrok_url))
    st.session_state.messages.append({"role": model, "content": response})

def get_response(model, prompt, url):
    model_gemma = ChatOllama(
        model=model, temperature=0, base_url=url, verbose=True
    )
    return model_gemma.stream(prompt)

def response_component_ft(model, prompt):
    with st.chat_message(model):
        with st.spinner("대답 중 ..."):
          data = {
            'prompt': prompt,
            'max_tokens': 256
          }
          json_data = json.dumps(data)
          response = st.write(requests.post(vllm_ngrok_url, data = json_data,
                                   headers = {'Content-Type': 'application/json'}))
    st.session_state.messages.append({"role": model, "content": response})

  # history_llm_format.append({"role": "assistant", "content": response.json()})
  # return history_llm_format


with st.sidebar:
    ollama_ngrok_url = st.text_input("Ollama Ngrok URL", key="ollama_ngrok_url")
    vllm_ngrok_url = st.text_input("Vllm Ngrok URL", key="vllm_ngrok_url")


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
    response_component(finetuned, prompt)
    # response_component(gemma, prompt)
    # response_component(llama, prompt)

    # if vllm_ngrok_url:
    #     response_component_ft(finetuned, prompt)

