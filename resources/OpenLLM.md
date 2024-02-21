**OpenLLM** is an open platform for operating large language models (LLMs) in production. It enables developers to easily run inference with any open-source LLMs, deploy to the cloud or on-premises, and build powerful AI apps.

**Prerequisites:**
- You have installed Python 3.8 (or later) and pip. We highly recommend using a Virtual Environment to prevent package conflicts.

**Create a Python Virtual Environment:**
1. Navigate to your project directory
```bash
cd /path_to_your_project
```

2. Create a virtual environment
```bash
python -m venv venv
```

3. Activate the virtual environment by running:
```bash
.\venv\Scripts\activate
```


**Install OpenLLM:**
Install OpenLLM by using pip as follows:
```bash
pip install openllm
```


**Start an LLM server:**
OpenLLM allows you to quickly spin up an LLM server using `[openllm start]`. For example, to start an OPT server, run the following:
```bash
openllm start opt
```

This starts the server at `[http://0.0.0.0:3000/]`.

To interact with the server, you can visit the web UI at `[http://0.0.0.0:3000/]` or send a request using `curl`. You can also use OpenLLM's built-in Python client to interact with the server:
```python
import openllm
client = openllm.client.HTTPClient('http://localhost:3000')
client.query('Explain to me the difference between "further" and "farther"')
```

OpenLLM supports many models and their variants. You can specify different variants of the model to be served by providing the --model-id option. For example:
```bash
openllm start opt --model-id facebook/opt-2.7b
```

## LLM models Installation

OpenLLM currently supports the many models. By default, OpenLLM doesn't include dependencies to run all models. The extra model-specific dependencies can be installed with the instructions below.

Llama Installation:
To run Llama models with OpenLLM, you need to install the llama dependency as it is not installed by default.
```bash
pip install "openllm[llama]"
```

Run the following commands to quickly spin up a Llama 2 server and send a request to it.

```bash
openllm start llama --model-id meta-llama/Llama-2-7b-chat-hf
export OPENLLM_ENDPOINT=http://localhost:3000
openllm query 'What are large language models?'
```

you can install different models using the same approach

if you want to install a model manually, you can download your desired model and move it to this directory:

```bash
C:\Users\LENOVO\bentoml\models
```
You need to replace 'LENOVO' with your computer's username

## Quantization

Quantization is a technique to reduce the storage and computation requirements for machine learning models, particularly during inference. By approximating floating-point numbers as integers (quantized values), quantization allows for faster computations, reduced memory footprint, and can make it feasible to deploy large models on resource-constrained devices.

OpenLLM supports quantization through two methods - bitsandbytes and GPTQ.

To run a model using the bitsandbytes method for quantization, you can use the following command:

```bash
openllm start opt --quantize int8
```

## LangChain
To quickly start a local LLM with langchain, simply do the following:

```python
from langchain.llms import OpenLLM
llm = OpenLLM(model_name="llama", model_id='meta-llama/Llama-2-7b-hf')
llm("What is the difference between a duck and a goose? And why there are so many Goose in Canada?")
```

## Docker container
Building a Bento: With OpenLLM, you can easily build a Bento for a specific model, like dolly-v2, using the build command.:

```bash
openllm build dolly-v2
```



## Now we'll see how to install OpenLLM and use it on Télécom GPUs

1. Connect to Télécom Paris network using OpenVPN GUI. Follow the steps [here](https://eole.telecom-paris.fr/vos-services/services-numeriques/connexions-aux-reseaux/openvpn-avec-windows).

2. Connect by SSH to Télécom GPUs. See how to do it [here](https://eole.telecom-paris.fr/vos-services/services-numeriques/connexions-aux-reseaux/openvpn-avec-windows).

3. `pip install openllm`
4. Verify installation with `openllm -h`
5. openllm is installed in `~/.local/bin`. Go into that directory
6. `./openllm start` allows you to see the LLMservers that you can launch. Make sure to book a GPU first using `CUDA_VISIBLE_DEVICES=0` for example.


## advices and solutions to errors : 

If you have an "can't bind to localhost:3000 error, kill all your process that are on port 3000.

run your servers using vllm background using `--backend vllm` because otherwise, it would py PyTorch, and vllm is faster and optimized for LLMs


résoudre `[ERROR] [cli] Could not bind 0.0.0.0:3000` : 
`lsof -t -i:3000 | xargs kill -9`

Once you're done, you can make sure to kill all the process by using `!pkill -f 'bentoml|openllm'`
