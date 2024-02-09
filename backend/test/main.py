import os
import sys
import torch


backend_folder = f"{os.getcwd()}/backend"

sys.path.append(backend_folder)


from llm.llm_model import LlmModel
from embedding.rag_wrapper import RagWrapper
from langchain_wrapper.lang_wrapper import LangWrapper
from llm.model_names import code_llama_model_13b_instruct, mistral_model, starcoder
from utils.main import select_gpu_if_available

model_name = starcoder

def move_tensors_to_gpu(obj):
    if isinstance(obj, torch.Tensor):
        if obj.device.type != 'cuda':
            obj = obj.to('cuda')
    if hasattr(obj, '__dict__'):
        for attr_name in obj.__dict__:
            attr = getattr(obj, attr_name)
            setattr(obj, attr_name, move_tensors_to_gpu(attr))
    if hasattr(obj, '__iter__'):
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = move_tensors_to_gpu(value)
        else:
            for i, item in enumerate(obj):
                obj[i] = move_tensors_to_gpu(item)
    return obj



def main():
    while True:
        # model
        model = LlmModel(model_name=model_name)
        print("model device after init :", model.model.hf_device_map)

        # rag
        repo_url = "https://github.com/esphome/esphome"
        branch = "dev"
        file_type = ".py"
        ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)

        # langchain
        langchain_wrapper = LangWrapper(model=model)
        langchain_wrapper.add_rag_wrapper(ragWrapper)
        langchain_wrapper.setup_rag_llm_chain()


        #move_tensors_to_gpu(langchain_wrapper)

        question = """
            Briefly tell me what the codegen.py file does
            """
        generated_text = langchain_wrapper.invoke_llm_chain(question)
        history = generated_text["chat_history"]  # type: ignore
        # gen_text = model.generate_text(question)
        print(generated_text["answer"])  # type: ignore

        question = """
            output EXATCLY the COMPLETE code of 'iter_components' function AS IS
            """
        generated_text = langchain_wrapper.invoke_llm_chain(question=question)

        # gen_text = model.generate_text(question)
        print(generated_text["answer"])  # type: ignore

        question = """
            what is the path of a02yyuw.cpp file in the repository ?
            """
        generated_text = langchain_wrapper.invoke_llm_chain(question=question)

        # gen_text = model.generate_text(question)
        print(generated_text["answer"])  # type: ignore

        langchain_wrapper.cleanup()


if __name__ == "__main__":
    main()
