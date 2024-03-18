import torch
from langchain.llms import OpenLLM
torch.FloatTensor(0).to('cuda')
llm = OpenLLM(model_name='mistral', model_id='mistralai/Mistral-7B-Instruct-v0.1')
llm('What is a goose ?')
