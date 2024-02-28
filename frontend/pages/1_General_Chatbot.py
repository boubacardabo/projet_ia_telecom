import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.llms import OpenLLM
import requests
import os

backend_url = os.environ.get("API_URL") or "http://localhost:4000"
st.session_state["is_setup"] = False
use_case_name = "general_chatbot"

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
            "use_case": use_case_name,
            "has_rag": input_visibility[selected_option],  # type: ignore
            "repo_url": repository_link,
            "branch": branch_name,
            "file_type": file_type,
        }
        with st.spinner(""):
            response = requests.post(f"{backend_url}/setup_use_case/", json=data)

            if use_case_name in response.text and response.status_code == 200:
                st.session_state["is_setup"] = True
                st.success("Your chat has been successfully set up")
            else:
                st.session_state["is_setup"] = False
                st.error(
                    f"An error has occurred during setup: {response.status_code} {response.text}"
                )

st.title("General RAG Chatbot🔎")


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi, I'm a chatbot who can search in the project files with Retrieval Augmented Generation (RAG). Please set me up on the sidebar before proceeding",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(
    placeholder="Ask a new question", disabled=(not st.session_state["is_setup"])
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        data = {"use_case": "general_chatbot", "question": prompt}
        with st.spinner(""):
            response = requests.post(f"{backend_url}/invoke_use_case/", json=data).text
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
