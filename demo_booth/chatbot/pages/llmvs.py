import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import time

st.set_page_config(layout="wide")
st.sidebar.page_link("home.py", label="Home")
st.sidebar.page_link("pages/dataset.py", label="Dataset")
st.sidebar.page_link("pages/prompts.py", label="Prompt")
st.sidebar.page_link("pages/finetuning.py", label="FT")
st.sidebar.page_link("pages/b2ft.py", label="B2FT")
st.sidebar.page_link("pages/llmvs.py", label="LLMvs")

# # 모델과 토크나이저 로드
# models = st.session_state.models
# tokenizer = st.session_state.get("tokenizer", None)

# if models is None or tokenizer is None:
#     st.error("모델이 로드되지 않았습니다. Home으로 돌아가 모델을 불러오세요.")
# else:
#     # 사용할 모델 선택
#     model3 = models[0]  # 예시로 모델 3 선택

#     # 대화 기록 및 타이머 초기화
#     if "messages" not in st.session_state.keys():
#         st.session_state.messages = [
#             {
#                 "role": "assistant",
#                 "content": "당신에게 삶의 북극성이 되는 목표는 무엇이죠?",
#             }
#         ]
#         st.session_state.cosine_scores = []  # 코사인 유사도 점수 기록용 리스트
#         st.session_state.timer_started = False
#         st.session_state.start_time = None

#     # Display or clear chat messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])

#     def clear_chat_history():
#         st.session_state.messages = [
#             {
#                 "role": "assistant",
#                 "content": "당신에게 삶의 북극성이 되는 목표는 무엇이죠?",
#             }
#         ]

#     st.sidebar.button("Clear Chat History", on_click=clear_chat_history)

#     # 응답 생성 함수
#     def generate_response(model, prompt, max_length=1000):
#         input_ids = tokenizer.encode(prompt, return_tensors="pt")
#         output = model.generate(
#             input_ids, max_length=max_length, pad_token_id=tokenizer.eos_token_id
#         )
#         # tokens = tokenizer.convert_ids_to_tokens(output[0], skip_special_tokens=True)
#         # for token in tokens:
#         #     st.write(token)
#         return tokenizer.decode(output[0], skip_special_tokens=True)

#     # Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
#     def generate_gemma_response(model, prompt_input):
#         string_dialogue = ""
#         for dict_message in st.session_state.messages:
#             if dict_message["role"] == "user":
#                 string_dialogue += (
#                     "<start_of_turn>user\n"
#                     + dict_message["content"]
#                     + "<end_of_turn>\n\n"
#                 )
#             else:
#                 string_dialogue += (
#                     "<start_of_turn>model\n "
#                     + dict_message["content"]
#                     + "<end_of_turn>\n\n"
#                 )
#             user_ask = dict_message["content"]
#         output = generate_response(
#             model,
#             f"<bos><start_of_turn>user\n{user_ask}<end_of_turn>\n\n<start_of_turn>model\n ",
#             max_length=1000,
#         )
#         return output

#     # User-provided prompt
#     if prompt := st.chat_input():
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)

#         # Generate a new response if last message is not from assistant
#         if st.session_state.messages[-1]["role"] != "assistant":
#             with st.chat_message("assistant"):
#                 with st.spinner("Thinking..."):
#                     response = generate_gemma_response(model3, prompt)
#                     # tokens = tokenizer.tokenize(response)
#                     # for token in tokens:
#                     st.write(response)  # 토큰 단위로 assistant의 답변 출력

#             message = {"role": "assistant", "content": response}
#             st.session_state.messages.append(message)


import streamlit as st
import time

# Display Streamlit content
st.title("당신 삶의 북극성은 무엇인가요?:star:")

import subprocess

aaa = subprocess.Popen(["gradio", "gradio_interface.py"])

# Replace the Gradio interface URL with your generated share link
gradio_interface_url = "https://736a167efcedddfb2d.gradio.live"  # Example URL

# Load the Gradio interface using an iframe
st.write(
    f'<iframe src="{gradio_interface_url}" width="1000" height="800"></iframe>',
    unsafe_allow_html=True,
)
