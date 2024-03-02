
from langchain_wrapper.lang_wrapper import LangWrapper
from llm.llm_model import LlmModel
from langchain_wrapper.lang_wrapper import LangWrapper
from embedding.rag_wrapper import RagWrapper
from prompt.prompts import prompt_usecase_test_unit



def setup_chat(
    model: LlmModel, has_rag: bool, repo_url=None, branch=None, file_type=None
):
    lang_wrapper = None
    if not has_rag:
        lang_wrapper = LangWrapper(llmModel=model, prompt=prompt_usecase_test_unit)
    else:
        assert repo_url
        assert file_type
        ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)
        lang_wrapper = LangWrapper(llmModel=model)
        lang_wrapper.add_rag_wrapper(ragWrapper)
        lang_wrapper.setup_rag_llm_chain()

    return lang_wrapper




def invoke_chat_unit_test(lang_wrapper: LangWrapper, function_string: str, specification_string:str):
        
    generated_text = lang_wrapper.invoke_llm_chain_code_writer_unit_test_usecase(function=function_string, specification=specification_string)

    return generated_text






