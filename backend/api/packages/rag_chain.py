from embedding.rag_wrapper import RagWrapper
from langchain_wrapper.lang_wrapper import LangWrapper
from llm.llm_model import LlmModel
from main import args
from prompt.prompts import prompt_template_RAG


# rag
repo_url = "https://github.com/esphome/esphome"
branch = "dev"
file_type = ".py"

ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)
llmModel = LlmModel(model_name=args.model_name, is_open_llm=args.is_open_llm)
langchain_wrapper = LangWrapper(llmModel=llmModel, prompt=prompt_template_RAG)
langchain_wrapper.add_rag_wrapper(ragWrapper)
langchain_wrapper.setup_rag_llm_chain()

chain = langchain_wrapper.llmChain