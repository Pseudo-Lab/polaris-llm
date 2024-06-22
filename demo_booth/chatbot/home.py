import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from huggingface_hub import login

# with open("chatbot/credential.txt", "r") as f:
#     hf_token = f.readlines()[0].strip()

# login(token=hf_token)

st.set_page_config(layout="wide")
st.sidebar.page_link("home.py", label="Home")
st.sidebar.page_link("pages/dataset.py", label="Dataset")
st.sidebar.page_link("pages/prompts.py", label="Prompt")
st.sidebar.page_link("pages/finetuning.py", label="FT")
st.sidebar.page_link("pages/b2ft.py", label="B2FT")
st.sidebar.page_link("pages/llmvs.py", label="LLMvs")

st.title("LLM 수다속에서 내 갈길가기")
# st.image("images/home_cat.jpeg", use_column_width=True)
