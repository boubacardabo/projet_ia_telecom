import os
import sys
import traceback
from dotenv import load_dotenv

backend_folder = f"{os.getcwd()}/backend"
sys.path.append(backend_folder)

# Load variables from the .env file into the environment
load_dotenv()

if "LANGCHAIN_API_KEY" in os.environ:
    os.environ["LANGCHAIN_TRACING_V2"] = 'true'
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_PROJECT"]= "PRIM-NXP"

from embedding.rag_wrapper import RagWrapper
from langchain_wrapper.lang_wrapper import LangWrapper
from llm.llm_model import LlmModel




def main():
    try:


        # rag
        repo_url = "https://github.com/esphome/esphome"
        branch = "dev"
        file_type = ".py"
        ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)

        choice = input("Choose HuggingFaceAPI ('h') or OpenLLM ('o'):\n ").lower().strip()




        if choice == 'h':

            print("You are using the huggingFace pipeline API.\n")

            from llm.model_names import code_llama_model_13b_instruct

            # model
            model_name = code_llama_model_13b_instruct
            model = LlmModel(model_name=model_name)


            # question = """
            #     Briefly tell me what the codegen.py file does
            #     """
            # generated_text = langchain_wrapper.invoke_llm_chain(question)
            # # history = generated_text["chat_history"]  # type: ignore
            # # gen_text = model.generate_text(question)
            # print(generated_text["answer"])  # type: ignore




            
        elif choice == 'o':

            print("You are using OpenLLM.\n")

            model = LlmModel(is_open_llm=True)


        else:
            print("Invalid choice. Exiting.")
            return
    


        # langchain
        langchain_wrapper = LangWrapper(llmModel=model)
        langchain_wrapper.add_rag_wrapper(ragWrapper)
        langchain_wrapper.setup_rag_llm_chain()

        question = """
            Briefly tell me what the codegen.py file does
            """
        generated_text = langchain_wrapper.invoke_llm_chain(question)
    
        # gen_text = model.generate_text(question)
        print(generated_text["answer"])  # type: ignore

        question = """
            Where is the location of the codegen.py file ?
            """
        generated_text = langchain_wrapper.invoke_llm_chain(question)

        # gen_text = model.generate_text(question)
        print(generated_text["answer"])  # type: ignore

        question = """
            Can I use the codegen file to generate code in Java ?
            """
        generated_text = langchain_wrapper.invoke_llm_chain(question)
        print(generated_text["answer"])  # type: ignore

        # question = """
        #     output EXATCLY the COMPLETE code of 'iter_components' function AS IS
        #     """
        # generated_text = langchain_wrapper.invoke_llm_chain(question)
        # question = """
        #     what is the path of a02yyuw.cpp file in the repository ?
        #     """
        # generated_text = langchain_wrapper.invoke_llm_chain(question=question)

        # # gen_text = model.generate_text(question)
        # print(generated_text["answer"])  # type: ignore

        langchain_wrapper.cleanup()
    
    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    main()
