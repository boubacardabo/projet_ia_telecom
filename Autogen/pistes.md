“AutoGen is a framework that enables the development of LLM applications using multiple agents that can converse with each other to solve tasks. AutoGen agents are customizable, conversable, and seamlessly allow human participation. They can operate in various modes that employ combinations of LLMs, human inputs, and tools.” (https://github.com/microsoft/autogen)

Normally, to use Autogen, you have to use Open AI models, and have an Open AI API key. However, this service is not free and additionally, the endgoal of is to use open-source LLMs with Autogen. Therefore, I tried to use open-source LLMs with Autogen.

To do that, it is necessary to have a server on which is runnning a LLM, to replace the OpenAI server that we won’t/can’t use. LMstudio is a software that allows developpers to run LLMs locaelly on their computers. Thanks to that, I was able to deploy a [localhost](http://localhost) server on my machine and make run a LLM on it. The LLM loaded occupies RAM memory, so I was constrained to choose relatively small and higly quantized models in order to physically have enough memory to run it without slowing too much my PC.

Then, I tried Autogen quickstart on the GitHub codespaces has it is suggested on the Autogen GitHub. I modified the OAI_CONFIG_LIST accordingly. however, i got error : 

raise error.APIConnectionError(
openai.error.APIConnectionError: Error communicating with OpenAI: HTTPConnectionPool(host='localhost', port=1234): Max retries exceeded with url: /v1/chat/completions (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7efffc614c40>: Failed to establish a new connection: [Errno 111] Connection refused'))

probably because the machine on which the code in codespace is running “can’t access” the [localhost](http://localhost) on my computer.

So, i tried to run it on my own PC instead of on Codespace. I had to make sure to open firewall access for LMstudio and make sure that the file of the code on my PC isn’t on protected Windows folders. I tried for a basic usecase “answering question”. It works, but sometimes the delay of the reply was so long that I got timeout error (my CPU isn’t fast enough for the local LLM to computthe response without timeout time). But sometimes, it worked.

Then, I tried I predefined Autogen usecase whre two agents are discussing, one writing code ,the other one executing code. Problem : the code doesn’t compile (**TypeError**: create() got an unexpected keyword argument 'api_type').

One problem : loading local models on my PC makes my PC slow, therefore my workflow is slow and kind of a struggle. Potential solution : run open-source LLM on Télécom machine, and access it. (Using ngork to access the [localhost](http://localhost) of the machine remotely).