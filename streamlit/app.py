import streamlit as st
from langchain_community.chat_models import ChatOllama
from openai import OpenAI
import threading
import asyncio
import base64
from streamlit_extras.stylable_container import stylable_container


st.set_page_config(layout="wide")
st.title("ChatGPT-like clone")

# client = OpenAI(base_url="http://localhost:11434/v1", api_key="needed-but-ignored")

# Initialize session state for left and right if not already done
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "llama3"
if "right" not in st.session_state:
    st.session_state["right"] = {"messages": [], "latest": None}
if "left" not in st.session_state:
    st.session_state["left"] = {"messages": [], "latest": None}

left, right = st.columns(2)

base_url = "https://fbbe-35-236-128-141.ngrok-free.app"  # ngrok로 생성한 url 넣는 부분, 변경필요
model_gemma = ChatOllama(model="gemma:7b-instruct", temperature=0, base_url=base_url)
model_llama = ChatOllama(model="llama3:8b", temperature=0, base_url=base_url)
st.markdown(
    """
<style>
hr {
    margin: -0.5em 0 0 0;
    background-color: red;
}
p.prompt {
    margin: 0;
    font-size: 14px;
}

div.stChatMessage :has(div[data-testid="chatAvatarIcon-assistant"]) {
    flex-direction: row-reverse;
    text-align: right;
}

img.spinner {
    margin: -1em 0 0 0;
}
</style>
""",
    unsafe_allow_html=True,
)

if not "messages1" in st.session_state:
    st.session_state.messages1 = []

if not "messages2" in st.session_state:
    st.session_state.messages2 = []

if not "input_disabled" in st.session_state:
    st.session_state.input_disabled = False


def clear_everything():
    st.session_state.messages1 = []
    st.session_state.messages2 = []
    st.session_state.input_disabled = False


def disable():
    st.session_state.input_disabled = True


with st.sidebar:
    with stylable_container(
        "blue",
        css_styles="""
        button {
            background-color: red;
            color: white;
        }""",
    ):
        st.button("New Chat :speech_balloon:", on_click=clear_everything)
    st.write("***")


model_1 = "gemma:7b"
model_2 = "llama3:8b"
col1, col2 = st.columns(2)
col1.write(f"# :blue[{model_1}]")
col2.write(f"# :red[{model_2}]")

body_1 = col1.empty()
body_2 = col2.empty()


async def run_prompt(placeholder, model, message_history):
    with placeholder.container():
        for message in message_history:
            chat_entry = st.chat_message(name=message["role"])
            chat_entry.write(message["content"])
        assistant = st.chat_message(name="assistant")
        # assistant.image("images/loading-gif.gif", width=25)

        with open("images/loading-gif.gif", "rb") as file:
            contents = file.read()
            data_url = base64.b64encode(contents).decode("utf-8")

        assistant.markdown(
            f"<img src='data:image/gif;base64,{data_url}' class='spinner' width='25' />",
            unsafe_allow_html=True,
        )

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        *message_history,
    ]
    stream = await client.chat.completions.create(
        model=model, messages=messages, stream=True
    )
    streamed_text = ""
    async for chunk in stream:
        chunk_content = chunk.choices[0].delta.content
        if chunk_content is not None:
            streamed_text = streamed_text + chunk_content
            with placeholder.container():
                for message in message_history:
                    chat_entry = st.chat_message(name=message["role"])
                    chat_entry.write(message["content"])
                assistant = st.chat_message(name="assistant")
                assistant.write(streamed_text)
    message_history.append({"role": "assistant", "content": streamed_text})


async def main():
    await asyncio.gather(
        run_prompt(body_1, model="g", message_history=st.session_state.messages1),
        run_prompt(body_2, model="l", message_history=st.session_state.messages2),
    )
    st.session_state.input_disabled = False


if ask is not None:
    if ask == "":
        st.warning("Please enter a prompt")
    else:
        st.session_state.messages1.append({"role": "user", "content": prompt})
        st.session_state.messages2.append({"role": "user", "content": prompt})
        asyncio.run(main())
