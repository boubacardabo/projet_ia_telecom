import streamlit as st
import os

with st.sidebar:
    langsmith_api_key = st.text_input(
        "Langsmith API Key", key="langchain_search_api_key_langsmith", type="password"
    )

os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"]= "PRIM-NXP"

st.title("NXP-PRIM")

