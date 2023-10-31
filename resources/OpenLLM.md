**OpenLLM** is an open platform for operating large language models (LLMs) in production. It enables developers to easily run inference with any open-source LLMs, deploy to the cloud or on-premises, and build powerful AI apps.

**Prerequisites:**
- You have installed Python 3.8 (or later) and pip. We highly recommend using a Virtual Environment to prevent package conflicts.

**Create a Python Virtual Environment:**
1. Navigate to your project directory
`cd /path_to_your_project`

2. Create a virtual environment
`python -m venv venv`

3. Activate the virtual environment by running:
`.\venv\Scripts\activate`


**Install OpenLLM:**
Install OpenLLM by using pip as follows:
`pip install openllm`


**Start an LLM server:**
OpenLLM allows you to quickly spin up an LLM server using `openllm start`. For example, to start an OPT server, run the following:
`openllm start opt`

This starts the server at `http://0.0.0.0:3000/`.

To interact with the server, you can visit the web UI at `http://0.0.0.0:3000/` or send a request using `curl`. You can also use OpenLLM's built-in Python client to interact with the server:
```python
import openllm
client = openllm.client.HTTPClient('http://localhost:3000')
client.query('Explain to me the difference between "further" and "farther"')

OpenLLM supports many models and their variants. You can specify different variants of the model to be served by providing the --model-id option. For example:
`openllm start opt --model-id facebook/opt-2.7b`
