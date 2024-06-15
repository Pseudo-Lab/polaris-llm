#https://yunwoong.tistory.com/227
import time
import streamlit as st
st.set_page_config(layout="wide")
st.sidebar.page_link("home.py", label="Home")
st.sidebar.page_link("pages/dataset.py", label="Dataset")
st.sidebar.page_link("pages/prompts.py", label="Prompt")
st.sidebar.page_link("pages/finetuning.py", label="FT")
st.sidebar.page_link("pages/b2ft.py", label="B2FT")
st.sidebar.page_link("pages/llmvs.py", label="LLMvs")

with st.form(key='random'):
    random_system_prompt = st.text_area(label="시스템 프롬프트", height=20, placeholder="임의의 프롬프트 입력",
                                        key="random_system_prompt")
    random_user_prompt = st.text_area(label="유저 프롬프트", height=10, key="random_user_prompt")
    submitted = st.form_submit_button('Send')

    def stream_data():
        str_ = f'{random_system_prompt}{random_user_prompt}'
        for w in str_:
            yield w + " "
            time.sleep(0.02)

    if submitted and random_user_prompt and random_user_prompt:
        with st.status("응답 생성 중...", expanded=True) as status:
            st.write_stream(stream_data)
            status.update(label="응답 생성 완료!", state="complete", expanded=True)


with st.form(key='gemma'):
    gemma_system_prompt = st.text_area(label="시스템 프롬프트", height=20, placeholder="gemma 프롬프트 입력",
                                       key="gemma_system_prompt")
    gemma_user_prompt = st.text_area(label="유저 프롬프트", height=10, key="gemma_user_prompt")
    submitted = st.form_submit_button('Send')

    def stream_data():
        str_ = f'{gemma_system_prompt}{gemma_user_prompt}'
        for w in str_:
            yield w + " "
            time.sleep(0.02)

    if submitted and gemma_system_prompt and gemma_user_prompt:
        with st.status("응답 생성 중...", expanded=True) as status:
            st.write_stream(stream_data)
            status.update(label="응답 생성 완료!", state="complete", expanded=True)

import gradio as gr

# Initialize the histories for each model
g_history = []
l_history = []
gft_history = []


# Gradio interface
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label="Chat History")
    msg = gr.Textbox(placeholder="당신의 꿈을 적어보세요", label="Your Message")
    clear = gr.ClearButton([msg, chatbot])
    # gemma_response = gr.Textbox(label="Gemma's Response", interactive=False)
    # llama_response = gr.Textbox(label="Llama's Response", interactive=False)
    # wizard_response = gr.Textbox(label="WizardLM's Response", interactive=False)

    def handle_submit(message, chat_history):
      global g_history, l_history, gft_history
      #g_response, l_response, gft_response, g_history, l_history ,gft_history = response_all(message, g_history, l_history, gft_history)
      g_response, l_response, g_history, l_history = response_all(message, g_history, l_history)
    
      
      g_score = calcuate_nli(message, g_response)
      l_score = calcuate_nli(message, l_reㅇsponse)
      #gft_score = calcuate_nli(message, gft_response)
      g_score_float = g_score.flatten().numpy()[0]
      l_score_float = l_score.flatten().numpy()[0]
      #gft_score_float = gft_score.flatten().numpy()[0]




      chat_history.append((message, 'Gemma: '  + g_response + f' (nli score: {round(g_score_float, 2)})'))
      chat_history.append((None, 'Llama: ' + l_response + f' (nli score: {round(l_score_float, 2)})'))
      #chat_history.append((None, 'GemmaSFT: ' + gft_response + f' (nli score: {round(gft_score_float, 2)})'))
      
      return "", chat_history

    msg.submit(handle_submit, [msg, chatbot], [msg, chatbot])

demo.launch(share=True)
