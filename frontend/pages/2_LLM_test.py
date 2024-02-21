import streamlit as st
from langchain_community.llms import OpenLLM

with st.sidebar:
    langsmith_api_key = st.text_input(
        "Langsmith API Key", key="langchain_search_api_key_langsmith", type="password"
    )


st.title("Test")


def generate_response(input_text):
    server_url = "http://localhost:3000"
    llm = OpenLLM(server_url=server_url, timeout=360)
    st.info(llm(input_text))


with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)
