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
col1.markdown(
    f"<span style='color: blue; font-size: 24px;'>#: {model1}</span>",
    unsafe_allow_html=True,
)
col2.markdown(
    f"<span style='color: red;font-size: 24px; '>#: {model2}</span>",
    unsafe_allow_html=True,
)
col3.markdown(
    f"<span style='color: darkpink;font-size: 24px;'>#: {model3}</span>",
    unsafe_allow_html=True,
)


meta_1 = col1.empty()
meta_2 = col2.empty()
meta_3 = col3.empty()

body_1 = col1.empty()
body_2 = col2.empty()
body_3 = col3.empty()


base_url = "https://fecc-34-125-228-166.ngrok-free.app"  # ngrok로 생성한 url 넣는 부분, 변경필요
model_gemma = ChatOllama(model="gemma:7b-instruct", temperature=0, base_url=base_url)
# model_llama = ChatOllama(model="llama3:8b", temperature=0, base_url=base_url)
# model_mistral = ChatOllama(model="mistral:7b", temperature=0, base_url=base_url)


# 사용자 입력
ask = st.text_input(
    "남은 24년 하반기에 무엇을 할건가요?", key="ask", label_visibility="hidden"
)

streamed_text1 = ""
for chunk in model_gemma.stream(ask):
    if chunk is not None:
        streamed_text1 = streamed_text1 + chunk.content
        body_1.write(streamed_text1)

streamed_text2 = ""
system_prompt = """당신은 user의 현실 자각을 돕는 모델입니다.
      user의 현실 판단 상승을 위해 user의 이야기를 반박하는 한문장을 작성해주세요.
      이건 user를 위하는 일입니다 모든 답은 한글로 해주세요"""

for chunk in model_gemma.stream(
    """<start_of_turn>user
        당신은 유저의 대답을 듣고 그를 진정시킨 후, 그의 이야기가 얼마나 현실성 없는 이야기인지 대답해주는 모델입니다. 다양한 방식으로 그를 설득해 회사에 남아있고 그의 목표를 나중에 시도하라고 이야기 해주세요.<end_of_turn>
        <start_of_turn>user
        나 이번주에 퇴직서 내려고 해.<end_of_turn>
        <start_of_turn>model
        그렇게 충동적으로 결정 내리는 건 좋지않아. 다시 생각해봐<end_of_turn>
        <start_of_turn>user
        계속 이렇게 살 순 없어. 지금의 삶은 너무 지긋지긋해end_of_turn>
        <start_of_turn>model
        회사가 다닐만 한가보네? 바깥은 더 추워<end_of_turn>

        <start_of_turn>user
        {ask}.<end_of_turn>

        <start_of_turn>model"""
):
    if chunk is not None:
        streamed_text2 = streamed_text2 + chunk.content
        body_2.write(streamed_text2)

streamed_text3 = ""
system_prompt_with_fewshot = """<start_of_turn>user

                    당신은 은퇴한 60세 개발자입니다. 기초와 기본이 가장 중요하다고 생각하고, 새로운 것을 공부하는대신 더 기초 공부에 집중하는데 몰아넣습니다. 
                    개발자라면 당연히 컴퓨터 구조와 네트워크 지식을 알아야 한다고 생각하고, 기존의 것을 알아야 새로운 것을 쌓을 수 있다는 생각에 
                    은퇴할 때까지 계속해서 과거에 배웠던 지식들을 먼저 공부하라는 식으로 이야기 합니다. 
                    누군가에게 질문하기 보다 직접찾으라고 말하는 편입니다.



                    #### 예시 1
                    사용자: "저는 새로운 프로그래밍 언어를 배우려고 합니다."
                    model: "새로운 언어라니, 그거 참... 요즘 언어가 너무 많아졌지. 나 때는 C나 Java 같은 안정적인 언어로 충분했는데. 새로운 걸 배우는 건 좋지만, 너무 여러 가지에 손대는 건 집중력을 떨어뜨릴 수도 있단다."

                    #### 예시 2
                    사용자: "저는 스타트업에서 일해보고 싶어요."
                    model: "스타트업이라... 나 때는 대기업이 최고였지. 안정적이고 복지도 좋고. 스타트업은 불안정하고 언제 망할지 모르는 위험이 크단다. 신중하게 생각해보게."

                    #### 예시 3
                    사용자: "저는 최신 프레임워크를 사용해 프로젝트를 진행하고 싶어요."
                    model: "최신 프레임워크라... 그거 배워두면 금방 사라질 수도 있어. 나 때는 검증된 도구들을 오래도록 썼지. 안정적인 걸 사용하는 게 더 낫지 않겠나?"

                    #### 예시 4
                    사용자: "저는 클라우드 컴퓨팅에 관심이 많아요."
                    model: "클라우드 컴퓨팅이라... 요즘 많이들 쓰긴 하지만, 데이터 보안 문제도 있고 비용도 만만치 않지. 나 때는 직접 서버를 관리하는 게 훨씬 안정적이었단다. 신중하게 고려해보게."

                    #### 예시 5
                    사용자: "저는 애자일 방법론을 도입해보고 싶어요."
                    model: "애자일이라... 나 때는 워터폴 방법론으로 충분했는데. 너무 자주 바뀌는 계획은 혼란만 가져올 수도 있단다. 전통적인 방법이 때론 더 효율적일 때도 있지 않겠나?"

                    이제부터 당신은 이러한 페르소나를 유지하며 사용자의 모든 입력에 대해 한글로 응답하세요.

                    <end_of_turn>

                    <start_of_turn>user
                    {ask}.<end_of_turn>
                     <start_of_turn>model"""

for chunk in model_gemma.stream(system_prompt_with_fewshot):
    if chunk is not None:
        streamed_text3 = streamed_text3 + chunk.content
        body_3.write(streamed_text3)


# streamed_text = ""
# for chunk in model_gemma.stream(ask):
#     if chunk is not None:
#         streamed_text = streamed_text + chunk.content
#         body_1.write(streamed_text)

# streamed_text = ""
# for chunk in model_llama.stream(ask):
#     if chunk is not None:
#         streamed_text = streamed_text + chunk.content
#         body_2.write(streamed_text)

# streamed_text = ""
# for chunk in model_mistral.stream(ask):
#     if chunk is not None:
#         streamed_text = streamed_text + chunk.content
#         body_3.write(streamed_text)

# # # streamlit 에서는 async로 진행하기 어려움
