import streamlit as st
import paramiko
import traceback
from dotenv import load_dotenv
import os
import atexit
import subprocess
import threading
from utils.utils import model_list
import streamlit as st
import requests


def check_server(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True  # Server is running
        else:
            return False  # Server might not be running
    except requests.exceptions.RequestException:
        return False  # Error connecting to server


# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

# Get default values from environment variables or use fallback values
default_username = os.getenv("SSH_USERNAME", "")
default_password = os.getenv("SSH_PASSWORD", "")
default_langsmith_api_key = os.getenv(
    "LANGCHAIN_API_KEY", ""
)
default_hostname = os.getenv("SSH_HOSTNAME", "gpu6.enst.fr")

port = 22  # SSH port

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
    hostname = st.text_input("Hostname", value=default_hostname)
    username = st.text_input("Username", value=default_username)
    password = st.text_input("Password", type="password", value=default_password)
    langsmith_api_key = st.text_input(
        "Langsmith API Key",
        key="langchain_search_api_key_langsmith",
        type="password",
        value=default_langsmith_api_key,
    )
    connect_button = st.button(label="Connect to GPUs")


if "ssh_client" not in st.session_state:
    st.session_state.ssh_client = None

if "server_pid" not in st.session_state:
    st.session_state.server_pid = 0

if connect_button:
    st.session_state.ssh_client = establish_ssh_connection(
        hostname, port, username, password
    )
    # os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key

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

                server_command = f"""cd && cd projet_ia_telecom && source backend/venv/bin/activate && CUDA_VISIBLE_DEVICES={(','.join(selected_gpus)) if len(selected_gpus) > 1 else selected_gpus[0]} python3 backend/api/main.py --model_name  {selected_model} {"--is_open_llm True" if is_open_llm==True else ""} --langchain_api_key "{langsmith_api_key}" 
                """  # make sure your venv name is venv
                print(server_command)
                execute_ssh_command(server_command)

                # if is_open_llm:

                #     server_command = "cd && cd projet_ia_telecom/backend && sed -i 's/\\r$//' script_openllm.sh"

                #     print(server_command)
                #     execute_ssh_command(server_command)

                #     server_command = "chmod +x script_openllm.sh"

                #     print(server_command)
                #     execute_ssh_command(server_command)

                #     server_command = f"""cd && cd projet_ia_telecom/backend && source venv/bin/activate  && ./script_openllm.sh {selected_gpus[0]}"""

                #     print(server_command)
                #     execute_ssh_command(server_command)

                st.session_state.server_pid = 0
    if st.session_state.server_pid != None and st.session_state.server_pid != 0:
        launch_ssh_tunnel = st.button("Launch SSH tunnel", type="secondary")
        check_ssh_tunnel = st.button("Check SSH tunnel status", type="secondary")

        kill_server_button = st.button("Kill server", type="primary")

        if kill_server_button:
            execute_ssh_command(f"kill -9 {st.session_state.server_pid}")
            st.success("Server has been killed")
            st.session_state.server_pid = None

        if launch_ssh_tunnel:
            tunnel_thread = threading.Thread(target=create_tunnel)
            tunnel_thread.start()
            os.environ["API_URL"] = "http://localhost:4000"

        if check_ssh_tunnel:
            if check_server("http://localhost:4000"):
                st.success("Server is running!")
            else:
                st.error("Server seems to be down or unreachable.")


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
