import streamlit as st
import paramiko
import traceback
from dotenv import load_dotenv
import os
import atexit
import subprocess
import threading
from utils.utils import model_list


# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

# Get default values from environment variables or use fallback values
default_username = os.getenv("SSH_USERNAME", "bdabo")
default_password = os.getenv("SSH_PASSWORD", "")
default_langsmith_api_key = os.getenv("LANGCHAIN_API_KEY", "")

port = 22  # SSH port

# setting LangSmith API keys
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "PRIM-NXP"

# Streamlit app
st.title("GPU access")


# Define function to establish SSH connection
@st.cache_resource
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
def execute_ssh_command(command):
    try:
        # Execute the command on the remote machine
        stdin, stdout, stderr = st.session_state.ssh_client.exec_command(command)

        # Read the output (if any)
        output = stdout.read().decode("utf-8")

        return output

    except Exception as e:
        return traceback.format_exc()


def create_tunnel():
    try:
        code = subprocess.run(
            [
                "ssh",
                "-L",
                "4000:127.0.0.1:7000",
                f"{username}@{hostname}",
            ]
        )
    except Exception as e:
        print(e)


# Sidebar inputs for SSH connection parameters
with st.sidebar:
    st.subheader("SSH Connection Parameters")
    hostname = st.text_input("Hostname", value="gpu4.enst.fr")
    username = st.text_input("Username", value=default_username)
    password = st.text_input("Password", type="password", value=default_password)
    langsmith_api_key = st.text_input(
        "Langsmith API Key",
        key="langchain_search_api_key_langsmith",
        type="password",
        value=default_langsmith_api_key,
    )
    connect_button = st.button(label="Connect to GPUs")
    os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key

if "ssh_client" not in st.session_state:
    st.session_state.ssh_client = None

if "server_pid" not in st.session_state:
    st.session_state.server_pid = 0

if connect_button:
    st.session_state.ssh_client = establish_ssh_connection(
        hostname, port, username, password
    )

# Button to execute command
if st.session_state.ssh_client:
    check_gpus_button = st.button("See GPU Status")
    check_server_status_button = st.button("Server Status")

    if check_gpus_button:
        with st.spinner("Executing command..."):
            output = execute_ssh_command("nvidia-smi")
            st.code(output)
    if check_server_status_button:
        with st.spinner("Checking Server Status"):
            output = execute_ssh_command("lsof -t -i:7000")
            if len(output) > 0:
                st.success(f"Server running on PID ={output}")
                st.session_state.server_pid = output
            else:
                st.info("Server is not running")
                st.session_state.server_pid = None

    if st.session_state.server_pid == None:
        with st.spinner(""):
            available_gpus = execute_ssh_command("nvidia-smi -L").split("\n")
            available_gpus = [
                gpu.split(":")[0].split(" ")[-1]
                for gpu in available_gpus
                if gpu.startswith("GPU")
            ]

            st.subheader("GPU Selection for Server Launch")
            selected_gpus = st.multiselect(
                "Choose GPUs:",
                available_gpus,
            )
            selected_model = st.selectbox(label="Select Model", options=model_list)
            is_open_llm = st.checkbox("Use OpenLLM", value=False)

            launch_server_button = st.button("Launch Server")
            if launch_server_button:
                server_command = f"""cd && cd projet_ia_telecom &&
                source backend/venv/bin/activate && 
                CUDA_VISIBLE_DEVICES={(','.join(selected_gpus)) if len(selected_gpus) > 1 else selected_gpus[0]} python3 backend/api/main.py --model_name {selected_model if not is_open_llm else ""} {"--is_open_llm" if is_open_llm else ""}
                """
                print(server_command)
                execute_ssh_command(server_command)
                st.session_state.server_pid = 0
    if st.session_state.server_pid != None and st.session_state.server_pid != 0:
        launch_ssh_tunnel = st.button("Launch SSH tunnel", type="secondary")
        kill_server_button = st.button("Kill server", type="primary")

        if kill_server_button:
            execute_ssh_command(f"kill -9 {st.session_state.server_pid}")
            st.success("Server has been killed")
            st.session_state.server_pid = None

        if launch_ssh_tunnel:
            tunnel_thread = threading.Thread(target=create_tunnel)
            tunnel_thread.start()
            os.environ["API_URL"] = "http://localhost:4000"


# Cleanup function to close SSH connection when Streamlit app is stopped
def cleanup():
    if st.session_state.ssh_client:
        st.session_state.ssh_client.close()
    print(
        "SSH connection closed."
    )  # you can verify it in the log of the terminal from which you leaunched streamlit


# Register cleanup function
atexit.register(cleanup)

##################
