from langchain.llms import OpenLLM
import torch
torch.FloatTensor(0).to('cuda')
server_url = "http://localhost:3000"
llm = OpenLLM(server_url=server_url)
llm('What is a goose ?')
