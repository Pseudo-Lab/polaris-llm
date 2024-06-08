import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.sidebar.page_link("home.py", label="Home")
st.sidebar.page_link("pages/dataset.py", label="dataset")
st.sidebar.page_link("pages/prompt.py", label="prompt")
st.sidebar.page_link("pages/finetuning.py", label="finetuning")

components.iframe("http://52.53.194.4:5000", height=1000, width=1500)