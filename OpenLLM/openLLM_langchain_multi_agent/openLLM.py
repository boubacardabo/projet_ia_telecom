import openllm

llm = openllm.LLM('mistralai/Mistral-7B-Instruct-v0.1', backend='vllm', torch_dtype='float16', embedded=True)
