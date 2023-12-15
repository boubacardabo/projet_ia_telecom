# pip install "git+https://github.com/bentoml/langchain.git@chore/migrate-to-new-api#subdirectory=libs/langchain"
#modify openllm.py file in at location /.local/lib/python3.10/site-packages/langchain_community/llms accordingly (https://github.com/langchain-ai/langchain/blob/3d94cfdaf0c82ab67849f9e0b6a120654193025c/libs/community/langchain_community/llms/openllm.py)
# make sure to launch an openllm server before : openllm start <your model>
# then launch this file : CUDA_VISIBLE_DEVICES=0 python3 langchain_openllm_test.py
# works with :
# - OpenLLM version: 0.4.34
# - Langchain version : 0.0.339rc3 (fork of Langchain)
# launch


from langchain.llms import OpenLLM
import torch
torch.FloatTensor(0).to('cuda') #To change depending of the GPU you are using
server_url = "http://localhost:3000"
input = "What is the difference between a cat and a dog ?"
llm = OpenLLM(server_url=server_url)
(print(llm.invoke(input)))     

