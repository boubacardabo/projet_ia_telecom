import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.llms import OpenLLM


with st.sidebar:
    st.subheader("Chatbot parameters")
    options = ["Use RAG", "Use Normal Chatbot"]
    input_visibility = {"Use RAG": True, "Use Normal Chatbot": False}
    selected_option = st.selectbox("Toggle Input Visibility", options)
    if input_visibility[selected_option]:  # type: ignore
        repository_link = st.text_input(
            "Repository Link", value="https://github.com/esphome/esphome"
        )
        branch = st.text_input("Branch name for checkout", value="dev")
        file_type = st.text_input("File type for rag", value=".py")

    setup_button = st.button("Setup Chat")
    if setup_button:
        


st.title("General RAG Chatbot🔎")


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi, I'm a chatbot who can search in the project files with Retrieval Augmented Generation (RAG). How can I help you?",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What does the class PinRegistry do ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    server_url = "http://localhost:3000"
    llm = OpenLLM(server_url=server_url, timeout=360)

    retriever = ...
    search_agent = initialize_agent(
        [retriever],
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
