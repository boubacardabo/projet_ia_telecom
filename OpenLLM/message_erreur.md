```bash
./openllm start mistralai/Mistral-7B-Instruct-v0.1
```

It is recommended to specify the backend explicitly. Cascading backend might lead to unexpected behaviour.
Traceback (most recent call last):
  File "/home/infres/benrhouma-22/.local/bin/./openllm", line 8, in <module>
    sys.exit(cli())
  File "/home/infres/benrhouma-22/.local/lib/python3.10/site-packages/click/core.py", line 1157, in __call__
    return self.main(*args, **kwargs)
  File "/home/infres/benrhouma-22/.local/lib/python3.10/site-packages/click/core.py", line 1078, in main
    rv = self.invoke(ctx)
  File "/home/infres/benrhouma-22/.local/lib/python3.10/site-packages/click/core.py", line 1688, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "/home/infres/benrhouma-22/.local/lib/python3.10/site-packages/click/core.py", line 1434, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/home/infres/benrhouma-22/.local/lib/python3.10/site-packages/click/core.py", line 783, in invoke
    return __callback(*args, **kwargs)
  File "/home/infres/benrhouma-22/.local/lib/python3.10/site-packages/openllm_cli/entrypoint.py", line 204, in wrapper
    return_value = func(*args, **attrs)
  File "/home/infres/benrhouma-22/.local/lib/python3.10/site-packages/click/decorators.py", line 33, in new_func
    return f(get_current_context(), *args, **kwargs)
  File "/home/infres/benrhouma-22/.local/lib/python3.10/site-packages/openllm_cli/entrypoint.py", line 183, in wrapper
    return f(*args, **attrs)
  File "/home/infres/benrhouma-22/.local/lib/python3.10/site-packages/openllm_cli/entrypoint.py", line 415, in start_command
    llm = openllm.LLM[t.Any, t.Any](
  File "/usr/lib64/python3.10/typing.py", line 957, in __call__
    result = self.__origin__(*args, **kwargs)
  File "/home/infres/benrhouma-22/.local/lib/python3.10/site-packages/openllm/_llm.py", line 182, in __init__
    quantise=getattr(self._Quantise, backend)(self, quantize),
TypeError: getattr(): attribute name must be string
