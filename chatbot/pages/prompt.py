#https://yunwoong.tistory.com/227
import time
import streamlit as st
st.set_page_config(layout="wide")
st.sidebar.page_link("home.py", label="Home")
st.sidebar.page_link("pages/dataset.py", label="Dataset")
st.sidebar.page_link("pages/prompt.py", label="Prompt")
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

