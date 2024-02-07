import os
import sys
import torch


backend_folder = f"{os.getcwd()}/backend"

sys.path.append(backend_folder)


from llm.llm_model import LlmModel
from embedding.rag_wrapper import RagWrapper
from langchain_wrapper.lang_wrapper import LangWrapper
from llm.model_names import mistral_model


def main():
    try:
        # model
        model = LlmModel(model_name=mistral_model)

        # rag
        repo_url = "https://github.com/esphome/esphome"
        branch = "dev"
        file_type = ".py"
        ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)

        # langchain
        langchain_wrapper = LangWrapper(model=model)
        langchain_wrapper.add_rag_wrapper(ragWrapper)
        langchain_wrapper.setup_rag_llm_chain()
        question = """
            Briefly tell me what the codegen.py file does
            """
        generated_text = langchain_wrapper.invoke_llm_chain(question)
        # gen_text = model.generate_text(question)
        print(generated_text)

        question = """
            Give me the complete code in iter_components function
            """
        generated_text = langchain_wrapper.invoke_llm_chain(question)
        # gen_text = model.generate_text(question)
        print(generated_text)

        langchain_wrapper.cleanup()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
