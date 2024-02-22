import streamlit as st
import paramiko
import traceback
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))  

port = 22  # SSH

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


# Streamlit app
st.title("GPU access")


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

# Connect to SSH server (establish SSH connection only once)
client = establish_ssh_connection(hostname, port, username, password)

# Input for command to execute remotely
command = "nvidia-smi"

# Button to execute command
if st.button("See GPU Status"):
    with st.spinner("Executing command..."):
        output = execute_ssh_command(client, command)
        st.code(output)


