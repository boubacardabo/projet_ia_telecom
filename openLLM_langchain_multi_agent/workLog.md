using python 3.11.5
### Venv
pip3 install virtualenv
python3 -m venv nxp_venv
source nxp_venv/bin/activate

### OpenLLM
pip install openllm
pip install "openllm[vllm] doesn't work because vllm needs cuda, which needs us to be on a gpu

Runners in notebook
- LLM1: NousResearch/Nous-Hermes-llama-2-7b OK but very slow
- LLM2: facebook/opt-350m or 1.3b implementation issue with asyncio
Local server
- LLM1: NousResearch/Nous-Hermes-llama-2-7b OK but very slow
- LLM2: facebook/opt-350m or 1.3b OK in cli, but this error happened and the server went unresponsive 

2023-11-24T19:52:51+0100 [ERROR] [runner:llm-opt-runner:1] Traceback (most recent call last):

still receiving queries
Use it with no timeout. straight up hallucinates on everything

- LLM3: databricks/dolly-v2-3b  OK very good results with smal hallucination
- LLM4: google/flan-t5-small (77M) Implimentation issue
2023-11-24T20:50:36+0100 [ERROR] [api_server:llm-flan-t5-service:3] Exception in ASGI application 


### Install llm selectively 

use openllm.start to install the model you need
to kill the server: pkill -f 'bentoml|openllm'

### langchain one agent
first of all is to always set dtype as float32 for openllm in cpu mode as float16 only supported for gpu
restart your kernel when modifying local packages in a notebook context

got one result in code 
res GenerationOutput(prompt='What would be a good company name for a company that makes colorful socks?Answer in one word only', finished=True, outputs=[CompletionChunk(index=0, text=': Colorful Socks\n\nIf you were to start a company today, what would it be called?\n\nAnswer: Colorful Socks\n\nWhat would be your main selling point?\n\nAnswer: Colorful Socks\n\nWhat would be your main market?\n\nAnswer: Colors, Socks, & Cozy\n\nWhat would be your main product?\n\nAnswer: Colors, Socks, & Cozy\n\nWhat would be your main product category?\n\nAnswer: Colors, Socks, & Cozy\n\nWhat would be your main product category?\n\nAnswer: Colors,', token_ids=[35, 16858, 2650, 208, 6368, 50118, 50118, 1106, 47, 58, 7, 386, 10, 138, 452, 6, 99, 74, 24, 28, 373, 116, 50118, 50118, 33683, 35, 16858, 2650, 208, 6368, 50118, 50118, 2264, 74, 28, 110, 1049, 2183, 477, 116, 50118, 50118, 33683, 35, 16858, 2650, 208, 6368, 50118, 50118, 2264, 74, 28, 110, 1049, 210, 116, 50118, 50118, 33683, 35, 37780, 6, 208, 6368, 6, 359, 944, 5144, 50118, 50118, 2264, 74, 28, 110, 1049, 1152, 116, 50118, 50118, 33683, 35, 37780, 6, 208, 6368, 6, 359, 944, 5144, 50118, 50118, 2264, 74, 28, 110, 1049, 1152, 4120, 116, 50118, 50118, 33683, 35, 37780, 6, 208, 6368, 6, 359, 944, 5144, 50118, 50118, 2264, 74, 28, 110, 1049, 1152, 4120, 116, 50118, 50118, 33683, 35, 37780, 6, 6368, 6, 359, 944, 5144, 50118, 50118, 2264, 74, 28, 110, 1049, 1152, 4120, 116, 50118, 50118, 33683, 35, 37780, 6], cumulative_logprob=0.0, logprobs=None, finish_reason='length')], prompt_token_ids=[2, 2264, 74, 28, 10, 205, 138, 766, 13, 10, 138, 14, 817, 14128, 17753, 116, 33683, 11, 65, 2136, 129], prompt_logprobs=None, request_id='openllm-af235d1e2d4d41119377b265e10baa1b')

but timed out in the request with facebook/opt-1.3b

### langchain multi agent

