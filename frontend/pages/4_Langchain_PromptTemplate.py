import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenLLM

st.title("PRIM - NXP 🦜🔗")

openai_api_key = st.sidebar.text_input("Langsmith API Key", type="password")


def blog_outline(topic):
    # Instantiate LLM model
    server_url = "http://localhost:3000"
    llm = OpenLLM(server_url=server_url, timeout=360)
    # Prompt
    template = "As an experienced data scientist and technical writer, generate an outline for a blog about {topic}."
    prompt = PromptTemplate(input_variables=["topic"], template=template)
    prompt_query = prompt.format(topic=topic)
    # Run LLM model
    response = llm(prompt_query)
    # Print results
    return st.info(response)




with st.form("myform"):
    topic_text = st.text_input("Enter prompt:", "")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("You can add your Langsmith API key to continue to monitoring and debugging.")
    if submitted:
        blog_outline(topic_text)
