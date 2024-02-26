from backend.llm.llm_model import LlmModel

llmModel = LlmModel(is_open_llm=True)
chain = llmModel.model