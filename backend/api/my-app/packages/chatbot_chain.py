from backend.llm.llm_model import LlmModel
from backend.prompt.prompts import prompt_chatbot as prompt

llmModel = LlmModel(is_open_llm=True)
llm = llmModel.model

chain = prompt | llm
