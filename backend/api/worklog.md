test of rag_chain :



```
/home/infres/mcaillard-23/venv-test/lib/python3.10/site-packages/torch/_utils.py:831: UserWarning: TypedStorage is deprecated. It will be removed in the future and UntypedStorage will be the only storage class. This should only matter to you if you are using storages directly.  To access UntypedStorage directly, use tensor.untyped_storage() instead of tensor.storage()
  return self.fget.__get__(instance, owner)()
True
Process SpawnProcess-49:
Traceback (most recent call last):
  File "/usr/lib/python3.10/multiprocessing/process.py", line 314, in _bootstrap
    self.run()
  File "/usr/lib/python3.10/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "/home/infres/mcaillard-23/venv-test/lib/python3.10/site-packages/uvicorn/_subprocess.py", line 76, in subprocess_started
    target(sockets=sockets)
  File "/home/infres/mcaillard-23/venv-test/lib/python3.10/site-packages/uvicorn/server.py", line 61, in run
    return asyncio.run(self.serve(sockets=sockets))
  File "/usr/lib/python3.10/asyncio/runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "uvloop/loop.pyx", line 1517, in uvloop.loop.Loop.run_until_complete
  File "/home/infres/mcaillard-23/venv-test/lib/python3.10/site-packages/uvicorn/server.py", line 68, in serve
    config.load()
  File "/home/infres/mcaillard-23/venv-test/lib/python3.10/site-packages/uvicorn/config.py", line 467, in load
    self.loaded_app = import_from_string(self.app)
  File "/home/infres/mcaillard-23/venv-test/lib/python3.10/site-packages/uvicorn/importer.py", line 21, in import_from_string
    module = importlib.import_module(module_str)
  File "/usr/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 883, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/infres/mcaillard-23/backend/api/my-app/app/server.py", line 37, in <module>
    from packages.rag_chain import chain as ragChain
  File "/home/infres/mcaillard-23/backend/api/my-app/packages/rag_chain.py", line 23, in <module>
    langchain_wrapper.setup_rag_llm_chain()
  File "/home/infres/mcaillard-23/backend/langchain_wrapper/lang_wrapper.py", line 61, in setup_rag_llm_chain
    assert isinstance(self.ragWrapper, RagWrapper)
AssertionError

```

I tried : 

```
    def add_rag_wrapper(self, rag_wrapper: RagWrapper):
        self.ragWrapper = rag_wrapper
        assert isinstance(self.ragWrapper, RagWrapper)
```

and got an error at `assert isinstance(self.ragWrapper, RagWrapper)`, which is absurd.






```
ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)


llmModel = LlmModel(is_open_llm=True)

langchain_wrapper = LangWrapper(llmModel=llmModel)

# assert isinstance(ragWrapper, RagWrapper) #Success
# print(ragWrapper) #<backend.embedding.rag_wrapper.RagWrapper object at 0x7f24741ccdc0>

langchain_wrapper.add_rag_wrapper(ragWrapper)

```



```

    def add_rag_wrapper(self, rag_wrapper: RagWrapper):
        print(rag_wrapper) # <backend.embedding.rag_wrapper.RagWrapper object at 0x7f24741ccdc0> --> same address in memory.
        assert isinstance(rag_wrapper, RagWrapper) # fail. Conclusion : rag_wrapper mutated when it went into this function
        self.ragWrapper = rag_wrapper
```






if you get ``[Errno 98] Address already in use`` or ``accept: Too many open files ssh tunnel``, an easy way to get rid of it is to simply kill all process related to ssh : ``pkill ssh```. This error is maybe due to an accumulation of unclosed ssh tunnel or zombie processes.