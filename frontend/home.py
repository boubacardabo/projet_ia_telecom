import streamlit as st
import paramiko
import traceback
from dotenv import load_dotenv
import os
import atexit

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))  

port = 22  # SSH port


# Streamlit app
st.title("GPU access")



# Define function to establish SSH connection
def establish_ssh_connection(hostname, port, username, password):
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to SSH server
        client.connect(hostname, port, username, password)

        st.success("SSH connection established successfully.")

        return client  # Return the SSH client object

    except Exception as e:
        st.error(f"Error establishing SSH connection: {e}")
        st.stop()  # Stop Streamlit app if connection fails


# Define function to execute command on remote machine
def execute_ssh_command(client, command):
    try:
        # Execute the command on the remote machine
        stdin, stdout, stderr = client.exec_command(command)

        # Read the output (if any)
        output = stdout.read().decode('utf-8')

        return output

    except Exception as e:
        return traceback.format_exc()



# Get default values from environment variables or use fallback values
default_username = os.getenv("SSH_USERNAME", "username")
default_password = os.getenv("SSH_PASSWORD", "")
default_langsmith_api_key = os.getenv("LANGCHAIN_API_KEY", "")

# Sidebar inputs for SSH connection parameters
with st.sidebar:
    st.subheader("SSH Connection Parameters")
    hostname = st.text_input("Hostname", value="gpu6.enst.fr")
    username = st.text_input("Username", value=default_username)
    password = st.text_input("Password", type="password", value=default_password)
    langsmith_api_key = st.text_input("Langsmith API Key", key="langchain_search_api_key_langsmith", type="password", value=default_langsmith_api_key)

        
    
#setting LangSmith API keys
os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
os.environ["LANGCHAIN_PROJECT"]= "PRIM-NXP"


#SSH connection
ssh_client = establish_ssh_connection(hostname, port, username, password)


# Input for command to execute remotely
command = "nvidia-smi"

# Button to execute command
if st.button("See GPU Status"):
    with st.spinner("Executing command..."):
        output = execute_ssh_command(ssh_client, command)
        st.code(output)


# Cleanup function to close SSH connection when Streamlit app is stopped
def cleanup():
    ssh_client.close()
    print("SSH connection closed.") #you can verify it in the log of the terminal from which you leaunched streamlit

# Register cleanup function
atexit.register(cleanup)

##################

from langchain_community.llms import OpenLLM


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

##################

# import sys
# backend_folder = f"{os.getcwd()}/backend"
# sys.path.append(backend_folder)

# from langchain.agents import initialize_agent, AgentType
# from langchain.callbacks import StreamlitCallbackHandler

# from backend.embedding.rag_wrapper import RagWrapper
# from backend.langchain_wrapper.lang_wrapper import LangWrapper
# from backend.llm.llm_model import LlmModel

# # rag
# repo_url = "https://github.com/esphome/esphome"
# branch = "dev"
# file_type = ".py"
# ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)

# model = LlmModel(llm_runnable=True)

#  # langchain
# langchain_wrapper = LangWrapper(model=model)
# langchain_wrapper.add_rag_wrapper(ragWrapper)
# langchain_wrapper.setup_rag_llm_chain()


# st.title("Chat with RAG🔎")

# if "messages" not in st.session_state:
#     st.session_state["messages"] = [
#         {"role": "assistant", "content": "Hi, I'm a chatbot who can search in the project files with Retrieval Augmented Generation (RAG). How can I help you?"}
#     ]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input(placeholder="What does the class PinRegistry do ?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)


#     retriever = langchain_wrapper.ragWrapper.retriever

#     search_agent = initialize_agent(
#         [retriever], model.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True
#     )
#     with st.chat_message("assistant"):
#         st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
#         response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         st.write(response)

