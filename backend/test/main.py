import os
import sys
backend_folder = f"{os.getcwd()}/backend"
sys.path.append(backend_folder)
from embedding.rag_wrapper import RagWrapper
from langchain_wrapper.lang_wrapper import LangWrapper


def main():
    try:


        # rag
        repo_url = "https://github.com/esphome/esphome"
        branch = "dev"
        file_type = ".py"
        ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)

        

        os.environ["LANGCHAIN_TRACING_V2"] = 'true'
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        os.environ["LANGCHAIN_API_KEY"] = "ls__a21c5d9069a442c08645e82f0a7330cc"
        os.environ["LANGCHAIN_PROJECT"]= "PRIM-NXP"



        choice = input("Choose HuggingFacePipeline ('h') or OpenLLM ('o'): ").lower().strip()
        if choice == 'h':

            from llm.llm_model import LlmModel

            
            from llm.model_names import code_llama_model_13b_instruct

            # model
            model_name = code_llama_model_13b_instruct
            model = LlmModel(model_name=model_name)



            # langchain
            langchain_wrapper = LangWrapper(model=model)
            langchain_wrapper.add_rag_wrapper(ragWrapper)
            langchain_wrapper.setup_rag_llm_chain()

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




            
        elif choice == 'o':

            print("OpenLLM")


            from langchain_community.llms import OpenLLM

            server_url = "http://localhost:3000"
            llm = OpenLLM(server_url=server_url)

            langchain_wrapper = LangWrapper(model=llm)
            langchain_wrapper.add_rag_wrapper(ragWrapper)
            langchain_wrapper.setup_rag_llm_chain2()

            #question = input("How can I help you?").strip()
            question = """Briefly tell me what the codegen.py file does"""

            generated_text = langchain_wrapper.invoke_llm_chain2(question)
            print(generated_text['output_text'])


        else:
            print("Invalid choice. Exiting.")
            return
            

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
