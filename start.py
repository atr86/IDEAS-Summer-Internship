import transformers
import streamlit as st
from asr_module import show_asr_tab
from qa_module import show_qa_tab
from transformers import pipeline

st.set_page_config(
        page_icon='',
        page_title='IDEAS',
        layout='centered',
        initial_sidebar_state='auto'
    )

tab1, tab2 = st.tabs(["Speech to Text", "Question Answering"])
with tab1:
    st.header("🎙️Automatic Speech Recognition")
    show_asr_tab()

with tab2:
    st.header("📝Extractive Question Answering")
    if 'text' not in st.session_state:
        st.info("Transcribe atleast 1 audio")
    else:
        show_qa_tab()


