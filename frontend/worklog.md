Tried to implement RAG with the chatbot.
Problem : the embedding have to be done in GPU. Otherwise if I try to do it on CPU, I get this error :

```
Traceback (most recent call last):
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\backend\embedding\rag_wrapper.py", line 72, in loadSplitEmbedDocs
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\langchain_community\embeddings\huggingface.py", line 67, in __init__        
    self.client = sentence_transformers.SentenceTransformer(
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\sentence_transformers\SentenceTransformer.py", line 218, in __init__        
    self.to(device)
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\torch\nn\modules\module.py", line 1160, in to
    return self._apply(convert)
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\torch\nn\modules\module.py", line 810, in _apply
    module._apply(fn)
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\torch\nn\modules\module.py", line 810, in _apply
    module._apply(fn)
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\torch\nn\modules\module.py", line 810, in _apply
    module._apply(fn)
  [Previous line repeated 1 more time]
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\torch\nn\modules\module.py", line 833, in _apply
    param_applied = fn(param)
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\torch\nn\modules\module.py", line 1158, in convert
    return t.to(device, dtype if t.is_floating_point() or t.is_complex() else None, non_blocking)
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\torch\cuda\__init__.py", line 289, in _lazy_init
    raise AssertionError("Torch not compiled with CUDA enabled")
AssertionError: Torch not compiled with CUDA enabled

```

The idea is to do the embedding on GPU by luanching a script via SSH to hte remote machine, that will run a function that will create a Pickle file of the embedding (doable).

Then, from the frontend, fetch the Pickle file  (doable), and use it a an embedding object. I tried that, but then I got this error : 


```
Traceback (most recent call last):
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\backend\embedding\rag_wrapper.py", line 100, in loadSplitEmbedDocs
    db = Chroma.from_documents(texts, embeddings)
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\langchain_community\vectorstores\chroma.py", line 778, in from_documents
    return cls.from_texts(
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\langchain_community\vectorstores\chroma.py", line 736, in from_texts    
    chroma_collection.add_texts(
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\langchain_community\vectorstores\chroma.py", line 275, in add_texts
    embeddings = self._embedding_function.embed_documents(texts)
  File "D:\TSP\TSP_3A\projet_AI\projet_ia_telecom\venv\lib\site-packages\langchain_community\embeddings\huggingface.py", line 94, in embed_documents 
    texts, show_progress_bar=self.show_progress, **self.encode_kwargs
AttributeError: 'HuggingFaceEmbeddings' object has no attribute 'show_progress'

```


