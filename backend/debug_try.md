```Traceback (most recent call last):
  File "/home/infres/mcaillard-23/backend/test/main.py", line 64, in <module>
    main()
  File "/home/infres/mcaillard-23/backend/test/main.py", line 39, in main
    generated_text = langchain_wrapper.invoke_llm_chain(question)
  File "/home/infres/mcaillard-23/backend/langchain_wrapper/lang_wrapper.py", line 66, in invoke_llm_chain
    response = self.llmChain.invoke(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/base.py", line 162, in invoke
    raise e
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/base.py", line 156, in invoke
    self._call(inputs, run_manager=run_manager)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/conversational_retrieval/base.py", line 166, in _call
    answer = self.combine_docs_chain.run(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain_core/_api/deprecation.py", line 145, in warning_emitting_wrapper
    return wrapped(*args, **kwargs)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/base.py", line 543, in run
    return self(kwargs, callbacks=callbacks, tags=tags, metadata=metadata)[
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain_core/_api/deprecation.py", line 145, in warning_emitting_wrapper
    return wrapped(*args, **kwargs)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/base.py", line 363, in __call__
    return self.invoke(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/base.py", line 162, in invoke
    raise e
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/base.py", line 156, in invoke
    self._call(inputs, run_manager=run_manager)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/combine_documents/base.py", line 136, in _call
    output, extra_return_dict = self.combine_docs(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/combine_documents/stuff.py", line 244, in combine_docs
    return self.llm_chain.predict(callbacks=callbacks, **inputs), {}
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/llm.py", line 293, in predict
    return self(kwargs, callbacks=callbacks)[self.output_key]
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain_core/_api/deprecation.py", line 145, in warning_emitting_wrapper
    return wrapped(*args, **kwargs)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/base.py", line 363, in __call__
    return self.invoke(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/base.py", line 162, in invoke
    raise e
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/base.py", line 156, in invoke
    self._call(inputs, run_manager=run_manager)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/llm.py", line 103, in _call
    response = self.generate([inputs], run_manager=run_manager)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain/chains/llm.py", line 115, in generate
    return self.llm.generate_prompt(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain_core/language_models/llms.py", line 525, in generate_prompt
    return self.generate(prompt_strings, stop=stop, callbacks=callbacks, **kwargs)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain_core/language_models/llms.py", line 698, in generate
    output = self._generate_helper(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain_core/language_models/llms.py", line 562, in _generate_helper
    raise e
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain_core/language_models/llms.py", line 549, in _generate_helper
    self._generate(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/langchain_community/llms/huggingface_pipeline.py", line 203, in _generate
    responses = self.pipeline(batch_prompts)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/transformers/pipelines/text_generation.py", line 208, in __call__
    return super().__call__(text_inputs, **kwargs)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/transformers/pipelines/base.py", line 1121, in __call__
    outputs = list(final_iterator)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/transformers/pipelines/pt_utils.py", line 124, in __next__
    item = next(self.iterator)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/transformers/pipelines/pt_utils.py", line 125, in __next__
    processed = self.infer(item, **self.params)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/transformers/pipelines/base.py", line 1046, in forward
    model_outputs = self._forward(model_inputs, **forward_params)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/transformers/pipelines/text_generation.py", line 271, in _forward
    generated_sequence = self.model.generate(input_ids=input_ids, attention_mask=attention_mask, **generate_kwargs)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/torch/utils/_contextlib.py", line 115, in decorate_context
    return func(*args, **kwargs)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/transformers/generation/utils.py", line 1718, in generate
    return self.greedy_search(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/transformers/generation/utils.py", line 2579, in greedy_search
    outputs = self(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/transformers/models/gpt_bigcode/modeling_gpt_bigcode.py", line 1242, in forward
    transformer_outputs = self.transformer(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1518, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1527, in _call_impl
    return forward_call(*args, **kwargs)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/transformers/models/gpt_bigcode/modeling_gpt_bigcode.py", line 1025, in forward
    self_attention_mask = AttentionMaskConverter._unmask_unattended(
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/transformers/modeling_attn_mask_utils.py", line 238, in _unmask_unattended
    indices = torch.argmax(attention_mask.cpu() * tmp, 1, keepdim=True)
  File "/home/infres/mcaillard-23/.local/lib/python3.10/site-packages/torch/utils/_device.py", line 77, in __torch_function__
    return func(*args, **kwargs)
RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu!
```