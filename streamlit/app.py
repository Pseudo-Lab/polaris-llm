import streamlit as st
from langchain_community.chat_models import ChatOllama
import os
import asyncio
import threading
import time

# from token_count import TokenCount


title = "Polar basic chat"
st.set_page_config(page_title=title, layout="wide")
st.title(title)


model1 = "gemma:7b"
model2 = "gemma:7b + prompt"
model3 = "gemma:7b + prompt + fine-tuning"

col1, col2, col3 = st.columns(3)
col1.write(f"#: blue[{model1}]")
col2.write(f"#: red[{model2}]")
col3.write(f"#: pink[{model3}]")

meta_1 = col1.empty()
meta_2 = col2.empty()
meta_3 = col3.empty()

body_1 = col1.empty()
body_2 = col2.empty()
body_3 = col3.empty()


base_url = "https://fbbe-35-236-128-141.ngrok-free.app"  # ngrok로 생성한 url 넣는 부분, 변경필요
model_gemma = ChatOllama(model="gemma:7b-instruct", temperature=0, base_url=base_url)
model_llama = ChatOllama(model="llama3:8b", temperature=0, base_url=base_url)
model_mistral = ChatOllama(model="mistral:7b", temperature=0, base_url=base_url)

model_gemma._achat_stream_with_aggregation("안녕하세요")


# async def run_prompt(prompt, model, body, meta):
#     start = time.time()
#     stream = await model._achat_stream_with_aggregation(prompt)
#     streamed_text = ""
#     async for chunk in stream:
#         chunk_content = chunk.content
#         if chunk_content is not None:
#             streamed_text += chunk_content
#             body.write(streamed_text)
#             end = time.time()
#             time_taken = end - start
#             meta.info(
#                 f"""**고민시간: :green[{time_taken:.2f} secs]**
#             """
#             )

# / how to run async function in streamlit
# # https://discuss.streamlit.io/t/how-to-run-async-function-in-streamlit/1640


# async def main(ask):
#     await asyncio.gather(
#         run_prompt(ask, model_gemma, body_1, meta_1),
#         run_prompt(ask, model_llama, body_2, meta_2),
#         run_prompt(ask, model_mistral, body_3, meta_3),
#     )


ask = st.text_input(
    "남은 24년 하반기에 무엇을 할건가요?", key="ask", label_visibility="hidden"
)

if ask is not None:
    if ask == "":
        st.warning("질문을 입력해주세요")
    else:
        asyncio.run(main(ask))

streamed_text = ""
for chunk in model_gemma.stream(ask):
    if chunk is not None:
        streamed_text = streamed_text + chunk.content
        body_1.write(streamed_text)

streamed_text = ""
for chunk in model_llama.stream(ask):
    if chunk is not None:
        streamed_text = streamed_text + chunk.content
        body_2.write(streamed_text)

streamed_text = ""
for chunk in model_mistral.stream(ask):
    if chunk is not None:
        streamed_text = streamed_text + chunk.content
        body_3.write(streamed_text)

# streamlit 에서는 async로 진행하기 어려움
