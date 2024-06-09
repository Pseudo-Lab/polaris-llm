import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")
st.sidebar.page_link("home.py", label="Home")
st.sidebar.page_link("pages/dataset.py", label="Dataset")
st.sidebar.page_link("pages/prompt.py", label="Prompt")
st.sidebar.page_link("pages/finetuning.py", label="FT")
st.sidebar.page_link("pages/b2ft.py", label="B2FT")
st.sidebar.page_link("pages/llmvs.py", label="LLMvs")
# with st.sidebar:
#     selected = option_menu("Menu", ["Dataset", "Prompt", "FT", "B2FT", "LLMvs"],
#         icons=['house', 'gear', 'gear', 'gear', 'gear'], menu_icon="cast", default_index=0)
#
#     if selected == "Prompt":
#         st.switch_page("pages/prompt.py")
#
# import streamlit as st
#
# if st.button("Dataset"):
#     st.switch_page("pages/dataset.py")
# if st.button("Prompt):
#     st.switch_page("pages/page_1.py")
# if st.button("Page 2"):
#     st.switch_page("pages/page_2.py")