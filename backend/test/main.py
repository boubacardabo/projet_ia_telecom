import os
import sys
import torch


torch.FloatTensor(2).to('cuda') #To change depending of the GPU you are using

backend_folder = f"{os.getcwd()}/backend"
sys.path.append(backend_folder)


from llm.llm_model import LlmModel
from embedding.rag_wrapper import RagWrapper
from langchain_wrapper.lang_wrapper import LangWrapper
from llm.model_names import starcoder

model_name = starcoder

os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__10ce43b562744edc989ff4dc8ac73e35"
os.environ["LANGCHAIN_PROJECT"]= "pt-virtual-osmosis-36"  # if not specified, defaults to "default"


def main():
    if True : 

        # model
        model = LlmModel(model_name=model_name)


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
            Write a unit test for the gpio_base_schema method.
            """
        
        generated_text = langchain_wrapper.invoke_llm_chain(question=question)

        # gen_text = model.generate_text(question)

        print(generated_text)  # type: ignore



        langchain_wrapper.cleanup()



if __name__ == "__main__":
    main()
