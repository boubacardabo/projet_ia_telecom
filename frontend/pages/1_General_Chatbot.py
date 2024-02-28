import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.llms import OpenLLM
import requests
import os

backend_url = os.environ["API_URL"]

with st.sidebar:
    st.subheader("Chatbot parameters")
    options = ["Use RAG", "Use Normal Chatbot"]
    input_visibility = {"Use RAG": True, "Use Normal Chatbot": False}
    selected_option = st.selectbox("Do you wish to use RAG ?", options)
    if input_visibility[selected_option]:  # type: ignore
        repository_link = st.text_input(
            "Repository Link", value="https://github.com/esphome/esphome"
        )
        branch_name = st.text_input("Branch name for checkout", value="dev")
        file_type = st.text_input("File type for rag", value=".py")

    setup_button = st.button("Setup Chat")
    if setup_button:
        data = {
            "use_case": "general_chatbot",
            "has_rag": input_visibility[selected_option],  # type: ignore
            "repo_url": repository_link,
            "branch": branch_name,
            "file_type": file_type,
        }
        response = requests.post(f"{backend_url}/setup_use_case/", data=data)

        print("ok", response.text)

st.title("General RAG Chatbot🔎")


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi, I'm a chatbot who can search in the project files with Retrieval Augmented Generation (RAG). Please set me up on the sidebar before proceeding",
        }
    ]
