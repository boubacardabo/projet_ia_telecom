“[AutoGen](https://github.com/microsoft/autogen) is a framework that enables the development of LLM applications using multiple agents that can converse with each other to solve tasks. AutoGen agents are customizable, conversable, and seamlessly allow human participation. They can operate in various modes that employ combinations of LLMs, human inputs, and tools.” 

Normally, to use Autogen, you have to use Open AI models, and have an Open AI API key. However, this service is not free and additionally, the endgoal of is to use open-source LLMs with Autogen. Therefore, I tried to use open-source LLMs with Autogen.

To do that, it is necessary to have a server on which is runnning a LLM, to replace the OpenAI server that we won’t/can’t use. [LMstudio](https://lmstudio.ai/) is a software that allows developpers to run LLMs locaelly on their computers. Thanks to that, I was able to deploy a [localhost](http://localhost) server on my machine and make run a LLM on it. The LLM loaded occupies RAM memory, so I was constrained to choose relatively small and higly quantized models in order to physically have enough memory to run it without slowing too much my PC.

Then, I tried Autogen quickstart on the GitHub codespaces has it is suggested on the Autogen GitHub. I modified the OAI_CONFIG_LIST accordingly. modifying OAI_CONFIG_LIST is akin to modify list_config directly in the executed code. At the end of the day, list_config should look like this :

```python
config_list = [{
    "api_type" : "open_ai",
    "api_base" : "http://localhost:1234/v1",
    "api_key" : "NULL"
}
]
```

However, i got error : 

```
raise error.APIConnectionError(
openai.error.APIConnectionError: Error communicating with OpenAI: HTTPConnectionPool(host='localhost', port=1234): Max retries exceeded with url: /v1/chat/completions (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7efffc614c40>: Failed to establish a new connection: [Errno 111] Connection refused'))`
```

probably because the machine on which the code in codespace is running “can’t access” the localhost on my computer.

So, i tried to run it on my own PC instead of on Codespace. I had to make sure to open firewall access for LMstudio and make sure that the file of the code on my PC isn’t on protected Windows folders. I tried for a basic usecase “answering question”. It works, but sometimes the delay of the reply was so long that I got timeout error (my CPU isn’t fast enough for the local LLM to comput the response without timeout time). But sometimes, it worked. The simple code is [this](https://github.com/PromptEngineer48/AutoGPT_Local_LLMs/blob/main/app.py) one.



Then, I tried I predefined Autogen [usecase](https://github.com/microsoft/autogen/blob/main/notebook/agentchat_auto_feedback_from_code_execution.ipynb) whre two agents are discussing, one writing code ,the other one executing code. Problem : the code doesn’t compile.

```
in ConversableAgent.initiate_chat(self, recipient, clear_history, silent, **context)
    526 """Initiate a chat with the recipient agent.
    527 
    528 Reset the consecutive auto reply counter.
ref='c:\Users\tatia\anaconda3\envs\hugging-face\lib\site-packages\autogen\agentchat\conversable_agent.py:1'>1</a>;32m   (...)
    537         "message" needs to be provided if the `generate_init_message` method is not overridden.
    538 """
    539 self._prepare_chat(recipient, clear_history)
--> 540 self.send(self.generate_init_message(**context), recipient, silent=silent)
...
    263             msg = f"Missing required argument: {quote(missing[0])}"
    264     raise TypeError(msg)
--> 265 return func(*args, **kwargs)

TypeError: create() got an unexpected keyword argument 'api_type'
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output
```

Besides, I tried an [alternative](https://microsoft.github.io/autogen/blog/2023/07/14/Local-LLMs/) to LMstudio, by initiating an endpoint using ChastChat. By following the instructions, I can launch the server successfully using `python -m fastchat.serve.controller` as recommended. However, I got an error to launch the model worker using `python -m fastchat.serve.model_worker --model-path chatglm2-6b` : 

```
2023-11-08 11:36:06 | INFO | model_worker | args: Namespace(host='localhost', port=21002, worker_address='http://localhost:21002', controller_address='http://localhost:21001', model_path='chatglm2-6b', revision='main', device='cuda', gpus=None, num_gpus=1, max_gpu_memory=None, dtype=None, load_8bit=False, cpu_offloading=False, gptq_ckpt=None, gptq_wbits=16, gptq_groupsize=-1, gptq_act_order=False, awq_ckpt=None, awq_wbits=16, awq_groupsize=-1, enable_exllama=False, exllama_max_seq_len=4096, exllama_gpu_split=None, enable_xft=False, xft_max_seq_len=4096, xft_dtype=None, model_names=None, conv_template=None, embed_in_truncate=False, limit_worker_concurrency=5, stream_interval=2, no_register=False, seed=None, debug=False)  
2023-11-08 11:36:06 | INFO | model_worker | Loading the model ['chatglm2-6b'] on worker 7a6aba82 ...
2023-11-08 11:36:06 | ERROR | stderr | Traceback (most recent call last):
2023-11-08 11:36:06 | ERROR | stderr |   File "C:\Users\tatia\anaconda3\envs\hugging-face\lib\runpy.py", line 197, in _run_module_as_main
2023-11-08 11:36:06 | ERROR | stderr |     return _run_code(code, main_globals, None,
2023-11-08 11:36:06 | ERROR | stderr |   File "C:\Users\tatia\anaconda3\envs\hugging-face\lib\runpy.py", line 87, in _run_code
2023-11-08 11:36:06 | ERROR | stderr |     exec(code, run_globals)
2023-11-08 11:36:06 | ERROR | stderr |   File "D:\TSP\TSP_3A\projet AI\LocalLLMAutogen\FastChat\fastchat\serve\model_worker.py", line 361, in <module>
2023-11-08 11:36:06 | ERROR | stderr |     args, worker = create_model_worker()
2023-11-08 11:36:06 | ERROR | stderr |   File "D:\TSP\TSP_3A\projet AI\LocalLLMAutogen\FastChat\fastchat\serve\model_worker.py", line 333, in create_model_worker
2023-11-08 11:36:06 | ERROR | stderr |     worker = ModelWorker(
2023-11-08 11:36:06 | ERROR | stderr |   File "D:\TSP\TSP_3A\projet AI\LocalLLMAutogen\FastChat\fastchat\serve\model_worker.py", line 77, in __init__
2023-11-08 11:36:06 | ERROR | stderr |     self.model, self.tokenizer = load_model(
2023-11-08 11:36:06 | ERROR | stderr |   File "D:\TSP\TSP_3A\projet AI\LocalLLMAutogen\FastChat\fastchat\model\model_adapter.py", line 312, in load_model
2023-11-08 11:36:06 | ERROR | stderr |     model, tokenizer = adapter.load_model(model_path, kwargs)
2023-11-08 11:36:06 | ERROR | stderr |   File "D:\TSP\TSP_3A\projet AI\LocalLLMAutogen\FastChat\fastchat\model\model_adapter.py", line 757, in load_model
2023-11-08 11:36:06 | ERROR | stderr |     tokenizer = AutoTokenizer.from_pretrained(
2023-11-08 11:36:06 | ERROR | stderr |   File "C:\Users\tatia\anaconda3\envs\hugging-face\lib\site-packages\transformers\models\auto\tokenization_auto.py", line 796, in from_pretrained
2023-11-08 11:36:06 | ERROR | stderr |     raise ValueError(
2023-11-08 11:36:06 | ERROR | stderr | ValueError: Unrecognized configuration class <class 'transformers_modules.chatglm2-6b.configuration_chatglm.ChatGLMConfig'> to build an AutoTokenizer.
2023-11-08 11:36:06 | ERROR | stderr | Model type should be one of AlbertConfig, AlignConfig, BarkConfig, BartConfig, BertConfig, BertGenerationConfig, BigBirdConfig, BigBirdPegasusConfig, BioGptConfig, BlenderbotConfig, BlenderbotSmallConfig, BlipConfig, Blip2Config, BloomConfig, BridgeTowerConfig, BrosConfig, CamembertConfig, CanineConfig, ChineseCLIPConfig, ClapConfig, CLIPConfig, CLIPSegConfig, LlamaConfig, CodeGenConfig, ConvBertConfig, CpmAntConfig, CTRLConfig, Data2VecAudioConfig, Data2VecTextConfig, DebertaConfig, DebertaV2Config, DistilBertConfig, DPRConfig, ElectraConfig, ErnieConfig, ErnieMConfig, EsmConfig, FlaubertConfig, FNetConfig, FSMTConfig, FunnelConfig, GitConfig, GPT2Config, GPT2Config, GPTBigCodeConfig, GPTNeoConfig, GPTNeoXConfig, GPTNeoXJapaneseConfig, GPTJConfig, GPTSanJapaneseConfig, GroupViTConfig, HubertConfig, IBertConfig, IdeficsConfig, InstructBlipConfig, JukeboxConfig, Kosmos2Config, LayoutLMConfig, LayoutLMv2Config, LayoutLMv3Config, LEDConfig, LiltConfig, LlamaConfig, LongformerConfig, LongT5Config, LukeConfig, LxmertConfig, M2M100Config, MarianConfig, MBartConfig, MegaConfig, MegatronBertConfig, MgpstrConfig, MistralConfig, MobileBertConfig, MPNetConfig, MptConfig, MraConfig, MT5Config, MusicgenConfig, MvpConfig, NezhaConfig, NllbMoeConfig, NystromformerConfig, OneFormerConfig, OpenAIGPTConfig, OPTConfig, Owlv2Config, OwlViTConfig, PegasusConfig, PegasusXConfig, PerceiverConfig, PersimmonConfig, Pix2StructConfig, PLBartConfig, ProphetNetConfig, QDQBertConfig, RagConfig, RealmConfig, ReformerConfig, RemBertConfig, RetriBertConfig, RobertaConfig, RobertaPreLayerNormConfig, RoCBertConfig, RoFormerConfig, RwkvConfig, SeamlessM4TConfig, Speech2TextConfig, Speech2Text2Config, SpeechT5Config, SplinterConfig, SqueezeBertConfig, SwitchTransformersConfig, T5Config, TapasConfig, TransfoXLConfig, UMT5Config, ViltConfig, VisualBertConfig, VitsConfig, Wav2Vec2Config, Wav2Vec2ConformerConfig, WhisperConfig, XCLIPConfig, XGLMConfig, XLMConfig, XLMProphetNetConfig, XLMRobertaConfig, XLMRobertaXLConfig, XLNetConfig, XmodConfig, YosoConfig.

```


______________________________________________________________


<u> One problem </u> : loading local models on my PC makes my PC slow, therefore my workflow is slow and kind of a struggle. Potential solution : run open-source LLM on Télécom machine, and access it using [ngork](https://ngrok.com/) and OpenVPN to access the localhost of the machine remotely.
