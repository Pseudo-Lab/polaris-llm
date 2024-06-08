import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")
st.sidebar.page_link("home.py", label="Home")
st.sidebar.page_link("pages/dataset.py", label="dataset")
st.sidebar.page_link("pages/prompt.py", label="prompt")
st.sidebar.page_link("pages/finetuning.py", label="finetuning")
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