# LLM Project Resources



## Datasets
- [ethos-u-vela](https://github.com/nxp-imx/ethos-u-vela/tree/lf-5.15.71_2.2.0/ethosu/vela) - **[Python][2.03 MiB]** ethos-u-vela is the ML model compiler tool and used to compile a TFLite-Micro model into an optimised version for ethos-u NPU on iMX93 platform.
  
- [esphome](https://github.com/esphome/esphome) - **[Python][19.01 MiB]** ESPHome is a system to control your ESP8266/ESP32 by simple yet powerful configuration files and control them remotely through Home Automation systems. 
  
- [HamShield](https://github.com/EnhancedRadioDevices/HamShield) - **[C++][911.00 KiB]** HamShield Arduino Library and Example Sketches

- [freeCodeCamp](https://github.com/freeCodeCamp/freeCodeCamp) - **[JavaScript][386.81 MiB]** Freecodecamp JS codebase with jest test files
  
- [bootstrap](https://github.com/twbs/bootstrap) - **[JavaScript][230.64 MiB]** Bootstrap codebase that contains e2e and integration tests
  
- [FixEval](https://github.com/mahimanzum/FixEval) - **[Python][19.96 MiB]** Java and Python dataset for competitive programming bug fixing along with a comprehensive test suite
  
- [bugnet](https://huggingface.co/datasets/alexjercan/bugnet) - **[Python/C++][around 50 MB]** Dataset based on the CodeNet project and contains Python and C++ code submissions for online coding competitions

- [CodeSearchNet corpus](https://huggingface.co/datasets/code_search_net) - **[Go, Java, JS, PHP, Python, Ruby][3.71 GB]** dataset of 2 milllion (comment, code) pairs from opensource libraries hosted on GitHub. It contains code and documentation for several programming languages. A structured dataset.

## Pre-trained LLM Instances
- [Hugging Face Model Hub](https://huggingface.co/models) - Repository of pre-trained models compatible with the Transformers library.
  

## Research Papers
- [Teaching large language models to self-debug](https://www.semanticscholar.org/reader/9e3c493fb09dcd61bb05e8c5659f23327b7b6340) - In this work, they propose SELF-DEBUGGING, where they teach the large language model to debug its own predicted code via few-shot prompting.

- [StarCoder: may the source be with you!](https://arxiv.org/pdf/2305.06161.pdf) - 
StarCoder is a State-of-the-Art LLM for Code, which is interesting for software validation and debugging. Used the paper to see how to prompt with is with sentinel tokens. 

## Online Courses and Tutorials
- [Autogen: task solving](https://github.com/microsoft/autogen/blob/main/notebook/agentchat_auto_feedback_from_code_execution.ipynb) - made by the developpers of AutoGen, explains how to use it to execute, debug, or solve task through code generation.



## Models
- [Llama-2-13b](https://huggingface.co/meta-llama/Llama-2-13b-chat-hf) - Link to download LLama 2 model and additional infos about the model and use cases.
  
- [Falcon-40b](https://huggingface.co/TheBloke/falcon-40b-instruct-GPTQ) - Link to download falcon 40b and infos how to use it.
  
- [Mistral-7b](https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF) - Link to download mistral 7b.
  
- [Mistral-7b-sharded](https://huggingface.co/someone13574/Mistral-7B-v0.1-sharded) - mistral 7b sharded into 8 parts to make it easier to load on a typical RAM (I had too low of RAM).
  
- [Llama 2 in LangChain — FIRST Open Source Conversational Agent!](https://www.youtube.com/watch?v=6iHVJyX2e50) - You can follow the first two chapters of the video to see how to deploy the models within your code.

- [Mixtral-8x7B-Instruct-v0.1](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1) - Mixtral outperforms Llama 2 70B on most benchmarks with 6x faster inference. Handles a context of 32k token and It shows strong performance in code generation, which is something we are interested in.

## Tools and Libraries
- [LangChain](https://www.langchain.com/) - LangChain gives developers a framework to build context-aware, reasoning LLM‑powered applications easily.

- [LangSmith](https://docs.smith.langchain.com/) - LangSmith is a platform for building production-grade LLM applications.It lets you debug, test, evaluate, and monitor chains and intelligent agents built on any LLM framework and seamlessly integrates with LangChain, the go-to open source framework for building with LLMs.


## Code Repositories
- [OpenLLM](https://github.com/bentoml/OpenLLM) -  An open-source platform to run inference of open-source LLM locally.


## Related Articles and Blog Posts
- [Introduction to LangGraph: A Beginner’s Guide](https://medium.com/@cplog/introduction-to-langgraph-a-beginners-guide-14f9be027141) - LangGraph is a powerful tool for building stateful, multi-actor applications with Large Language Models (LLMs). It extends the LangChain library, allowing you to coordinate multiple chains (or actors) across multiple steps of computation in a cyclic manner. Might be useful to deal with complex software validation & debugging tasks.


## Other Resources
- [HuggingFace](https://huggingface.co/) - A platform where the machine learning community collaborates on models, datasets, and applications. Might be useful to get models and datasets, as well as for the LLM-powered application of the project.


- [BentoML](https://www.bentoml.com/) - BentoML is a framework for building reliable, scalable, and cost-efficient AI applications. It comes with everything you need for model serving, application packaging, and production deployment. Might be useful for the LLM-power application of the project. BentoML is an open-source platform (free to use). What costs money is their BentoCloud service that provides fully managed infrastructures for deploying BentoML

