from llm.llm_model import LlmModel
from langchain_wrapper.lang_wrapper import LangWrapper
from main import args
from prompt.prompts import prompt_template_simple

llmModel = LlmModel(model_name=args.model_name, is_open_llm=args.is_open_llm)
langchain_wrapper = LangWrapper(llmModel=llmModel, prompt=prompt_template_simple)

chain = langchain_wrapper.llmChain