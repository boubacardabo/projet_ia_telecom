import streamlit as st
import paramiko
import traceback
from dotenv import load_dotenv
import os
import atexit
from langserve import RemoteRunnable


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
    hostname = st.text_input("Hostname", value="gpu4.enst.fr")
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


from langchain.prompts import PromptTemplate
import sys

backend_folder = f"{os.getcwd()}"

#To access to backend modules
if backend_folder not in sys.path:
    sys.path.append(backend_folder)

#for modules in backend to access to other modules
if f"{backend_folder}\\backend" not in sys.path:
    sys.path.append(f"{backend_folder}\\backend")

#st.text(sys.path)

@st.cache_resource
def create_chain(system_prompt):

    # model = LlmModel(is_open_llm=True)
    # llm = model.model

    llm = RemoteRunnable("http://localhost:8000/llm/")

    # Template you will use to structure your user input before converting
    # into a prompt. Here, my template first injects the personality I wish to
    # give to the LLM before in the form of system_prompt pushing the actual
    # prompt from the user. Note that this chatbot doesn't have any memory of
    # the conversation. So we will inject the system prompt for each message.
    # The template is adapted for Mistral models.

    template = """
    <s>[INST]{}[/INST]</s>

    [INST]{}[/INST]
    """.format(system_prompt, "{question}")

    # We create a prompt from the template so we can use it with Langchain
    prompt = PromptTemplate(template=template, input_variables=["question"])

    # We create an llm chain with our LLM and prompt
    # llm_chain = LLMChain(prompt=prompt, llm=llm) # Legacy
    llm_chain = prompt | llm  # LCEL

    return llm_chain





# Create a header element
st.header("Chatbot")


# This sets the LLM's personality for each prompt.
system_prompt = st.text_area(
    label="System Prompt",
    value="You are a helpful AI assistant who answers questions in short sentences.",
    key="system_prompt")

# Create LLM chain to use for our chatbot.
llm_chain = create_chain(system_prompt)

# We store the conversation in the session state.
# This will be used to render the chat conversation.
# We initialize it with the first message we want to be greeted with.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I help you today?"}
    ]

if "current_response" not in st.session_state:
    st.session_state.current_response = ""

# We loop through each message in the session state and render it as
# a chat message.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# We take questions/instructions from the chat input to pass to the LLM
if user_prompt := st.chat_input("Your message here", key="user_input"):

    # Add our input to the session state
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    # Add our input to the chat window
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Pass our input to the LLM chain and capture the final responses.
    response = llm_chain.invoke({"question": user_prompt})

    # Add the response to the session state
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    # Add the response to the chat window
    with st.chat_message("assistant"):
        st.markdown(response)
