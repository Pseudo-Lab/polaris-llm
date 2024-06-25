import asyncio
import streamlit as st
from langchain_community.chat_models import ChatOllama
from chatbot_prompt.prompt import BASIC_PROMPT, FEWSHOT_PROMPT

title = "Polar basic chat"
st.set_page_config(page_title=title, layout="wide")
st.sidebar.page_link("home.py", label="Home")
st.sidebar.page_link("pages/dataset.py", label="Dataset")
st.sidebar.page_link("pages/prompts.py", label="Prompt")
st.sidebar.page_link("pages/finetuning.py", label="FT")
st.sidebar.page_link("pages/b2ft.py", label="B2FT")
st.sidebar.page_link("pages/llmvs.py", label="LLMvs")

col1, col2, col3 = st.columns(3)
col1.image("images/basic.png", caption="gemma:7b", use_column_width=True)
col2.image("images/prompt.png", caption="gemma:7b + prompt", use_column_width=True)
col3.image(
    "images/finetuning.png",
    caption="gemma:7b + prompt + fine-tuning",
    use_column_width=True,
)

meta_1 = col1.empty()
meta_2 = col2.empty()
meta_3 = col3.empty()

body_1 = col1.empty()
body_2 = col2.empty()
body_3 = col3.empty()

# 사용자 입력
# ask = st.text_input(label="Enter some text 👇", key="ask", label_visibility="hidden", placeholder="질문을 입력해주세요.")
ask = st.chat_input()
if ask:
    base_url = "https://4d1a-54-226-143-197.ngrok-free.app"  # ngrok로 생성한 url 넣는 부분, 변경필요
    model_gemma = ChatOllama(
        model="gemma:7b-instruct", temperature=0, base_url=base_url
    )

    async def get_response(body, ask):
        streamed_text = ""
        async for chunk in model_gemma.astream(ask):
            if chunk is not None:
                streamed_text += chunk.content
                body.write(streamed_text)

    async def main():
        await asyncio.gather(
            get_response(body_1, ask),
            get_response(body_2, BASIC_PROMPT.format(ask)),
            get_response(body_3, FEWSHOT_PROMPT.format(ask)),
        )

    asyncio.run(main())
