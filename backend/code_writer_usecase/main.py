import os
import sys
import traceback

backend_folder = f"{os.getcwd()}/backend"
sys.path.append(backend_folder)
sys.path.remove(f"{os.getcwd()}/backend/code_writer_usecase")


os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__a21c5d9069a442c08645e82f0a7330cc"
os.environ["LANGCHAIN_PROJECT"]= "PRIM-NXP"

from embedding.rag_wrapper import RagWrapper
from langchain_wrapper.lang_wrapper import LangWrapper




def main():
    try:


        # rag
        repo_url = "https://github.com/esphome/esphome"
        branch = "dev"
        file_type = ".py"
        # ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)

        choice = input("Choose HuggingFaceAPI ('h') or OpenLLM ('o'):\n ").lower().strip()






        if choice == 'h':

            print("You are using the huggingFace pipeline API.\n")


            from llm.llm_model import LlmModel
            from llm.model_names import code_llama_model_13b_instruct

            # model
            model_name = code_llama_model_13b_instruct
            model = LlmModel(model_name=model_name)


            # langchain
            langchain_wrapper = LangWrapper(model=model)
            #langchain_wrapper.add_rag_wrapper(ragWrapper)
            langchain_wrapper.setup_rag_llm_chain()

            question = """
                Briefly tell me what the codegen.py file does
                """
            generated_text = langchain_wrapper.invoke_llm_chain(question)
            history = generated_text["chat_history"]  # type: ignore
            gen_text = model.generate_text(question)
            print(generated_text["answer"])  # type: ignore




            
        elif choice == 'o':

            print("You are using OpenLLM.\n")


            from langchain_community.llms import OpenLLM

            server_url = "http://localhost:3000"
            llm = OpenLLM(server_url=server_url)


            from prompt.prompts import prompt1

            langchain_wrapper = LangWrapper(model=llm, prompt=prompt1)




        else:
            print("Invalid choice. Exiting.")
            return
    


        ####
        from utils.main import get_functions, extract_function_from_markdown, write_function_to_file, get_function_names, execute_generated_file
        from code_writer_usecase.specification_functions import specification_string


        #fetching the function as a string
        file_path = backend_folder + "/code_writer_usecase/functions.py"
        functions = get_functions(file_path)
        function_string = functions[0]

        #generating output of LLM
        generated_text = langchain_wrapper.invoke_llm_chain3(function=function_string, specification=specification_string)
        print(generated_text)
        print("\n --------------------------------------- \n")

        #extract the Python code out of the output
        function_code = extract_function_from_markdown(generated_text)


        #Write the function in the file function_AI_generated.py, containing import and PyTest launch
        if function_code: #if a some code has been found

            function_names = get_function_names(file_path)
            function_name = function_names[0]
            write_function_to_file(function_code, backend_folder + "/code_writer_usecase/function_AI_generated.py", function_name=function_name, backend_folder=backend_folder)
            print("Function code has been written to 'function_AI_generated.py'")
        else:
            print("No function code extracted from the Markdown string.")

    
        #file execution
        stdout, stderr, returncode = execute_generated_file(backend_folder + "/code_writer_usecase/function_AI_generated.py")
        print("Standard output:")
        print(stdout)
        print("Standard error:")
        print(stderr)
        print("Return code:")
        print(returncode)



        langchain_wrapper.cleanup()

    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    main()
