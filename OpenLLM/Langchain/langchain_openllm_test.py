# pip install "git+https://github.com/bentoml/langchain.git@chore/migrate-to-new-api#subdirectory=libs/langchain"
# make sure to launch an openllm server before : openllm start <your model>
# then launch this file : CUDA_VISIBLE_DEVICES=0 python3 langchain_openllm_test.py
# works with : 
# - OpenLLM version: 0.4.34
# - Langchain version : 0.0.339rc3
# launch


from langchain.llms import OpenLLM
import torch
torch.FloatTensor(0).to('cuda')
server_url = "http://localhost:3000"
llm = OpenLLM(server_url=server_url)
output = llm.generate(['tell me the difference between a duck and a goose.'])
print(output)