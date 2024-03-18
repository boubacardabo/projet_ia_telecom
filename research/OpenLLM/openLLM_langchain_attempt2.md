```bash
[mcaillard-23@gpu6]~% cat test_openllm_langchain2.py
import torch
from langchain.llms import OpenLLM
torch.FloatTensor(0).to('cuda')
llm = OpenLLM(model_name='mistral', model_id='mistralai/Mistral-7B-Instruct-v0.1')
llm('What is a goose ?')
[mcaillard-23@gpu6]~% CUDA_VISIBLE_DEVICES=0 python3 test_openllm_langchain2.py
INFO 11-21 16:16:00 llm_engine.py:72] Initializing an LLM engine with config: model='/home/infres/mcaillard-23/bentoml/models/vllm-mistralai--mistral-7b-instruct-v0.1/7ad5799710574ba1c1d953eba3077af582f3a773', tokenizer='/home/infres/mcaillard-23/bentoml/models/vllm-mistralai--mistral-7b-instruct-v0.1/7ad5799710574ba1c1d953eba3077af582f3a773', tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=32768, download_dir=None, load_format=auto, tensor_parallel_size=1, quantization=None, seed=0)
INFO 11-21 16:16:22 llm_engine.py:207] # GPU blocks: 9275, # CPU blocks: 2048
Traceback (most recent call last):
  File "/home/infres/mcaillard-23/test_openllm_langchain2.py", line 5, in <module>
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
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/llms/openllm.py", line 273, in _call
    res = self._runner(prompt, **config.model_dump(flatten=True))
TypeError: 'LLMRunner' object is not callable
```
