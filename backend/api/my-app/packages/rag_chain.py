from backend.embedding.rag_wrapper import RagWrapper
from backend.langchain_wrapper.lang_wrapper import LangWrapper
from backend.llm.llm_model import LlmModel


# rag
repo_url = "https://github.com/esphome/esphome"
branch = "dev"
file_type = ".py"

ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)

llmModel = LlmModel(is_open_llm=True)

langchain_wrapper = LangWrapper(llmModel=llmModel)
langchain_wrapper.add_rag_wrapper(ragWrapper)
langchain_wrapper.setup_rag_llm_chain()

chain = langchain_wrapper.llmChain