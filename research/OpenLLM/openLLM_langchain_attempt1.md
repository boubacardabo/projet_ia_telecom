```bash
[mcaillard-23@gpu6]~% cat test_openllm_langchain3.py
from langchain.llms import OpenLLM
import torch
torch.FloatTensor(0).to('cuda')
server_url = "http://localhost:3000"
llm = OpenLLM(server_url=server_url)
llm('What is a goose ?')
[mcaillard-23@gpu6]~% CUDA_VISIBLE_DEVICES=0 python3 test_openllm_langchain3.py
Traceback (most recent call last):
  File "/home/infres/mcaillard-23/test_openllm_langchain3.py", line 6, in <module>
    llm('What is a goose ?')
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/llms/base.py", line 876, in __call__
    self.generate(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/llms/base.py", line 656, in generate
    output = self._generate_helper(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/llms/base.py", line 544, in _generate_helper
    raise e
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/llms/base.py", line 531, in _generate_helper
    self._generate(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/llms/base.py", line 1053, in _generate
    self._call(prompt, stop=stop, run_manager=run_manager, **kwargs)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/llms/openllm.py", line 270, in _call
    ).responses[0]
AttributeError: 'Response' object has no attribute 'responses'
Exception ignored in: <function HTTPClient.__del__ at 0x7efbb215b9a0>
Traceback (most recent call last):
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/openllm_client/_http.py", line 94, in __del__
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/httpx/_client.py", line 1258, in close
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/httpx/_transports/default.py", line 240, in close
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/httpcore/_sync/connection_pool.py", line 324, in close
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/httpcore/_sync/connection.py", line 172, in close
TypeError: 'NoneType' object is not callable```
