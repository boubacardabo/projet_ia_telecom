import streamlit as st
from langchain_community.llms import OpenLLM

st.title("Test")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


def generate_response(input_text):
    server_url = "http://localhost:3000"
    llm = OpenLLM(server_url=server_url, timeout=360)
    st.info(llm(input_text))


with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)
