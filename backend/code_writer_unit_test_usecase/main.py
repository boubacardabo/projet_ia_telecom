import os
import sys
import traceback
from dotenv import load_dotenv


backend_folder = f"{os.getcwd()}/backend"
if backend_folder not in sys.path:
    sys.path.append(backend_folder)

path_to_remove = f"{os.getcwd()}/backend/code_writer_unit_test_usecase"
if path_to_remove in sys.path:
    sys.path.remove(path_to_remove)


# Load variables from the .env file into the environment
load_dotenv()

if "LANGCHAIN_API_KEY" in os.environ:
    os.environ["LANGCHAIN_TRACING_V2"] = 'true'
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_PROJECT"]= "PRIM-NXP"

from langchain_wrapper.lang_wrapper import LangWrapper
from llm.llm_model import LlmModel



def main():
    try:


        choice = input("Choose HuggingFaceAPI ('h') or OpenLLM ('o'):\n ").lower().strip()



        if choice == 'h':

            print("You are using the huggingFace pipeline API.\n")


            
            from llm.model_names import code_llama_model_13b_instruct

            # model
            model_name = code_llama_model_13b_instruct
            model = LlmModel(model_name=model_name)


            
        elif choice == 'o':

            print("You are using OpenLLM.\n")


            model = LlmModel(llm_runnable=True)

            




        else:
            print("Invalid choice. Exiting.")
            return
    
        from prompt.prompts import prompt_usecase_test_unit
        langchain_wrapper = LangWrapper(llmModel=model, prompt=prompt_usecase_test_unit)
        
        ####
        from utils.utils import get_functions, extract_function_from_markdown, write_function_to_file, get_function_names, execute_generated_file
        from code_writer_unit_test_usecase.specification_functions import specification_string


        #fetching the function as a string
        file_path = backend_folder + "/code_writer_unit_test_usecase/functions.py"
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
            file_path = backend_folder + "/code_writer_unit_test_usecase/function_AI_generated.py"
            write_function_to_file(function_code, file_path=file_path, function_name=function_name)
            print("Function code has been written to 'function_AI_generated.py'")
        else:
            print("No function code extracted from the Markdown string.")

    
        #file execution
        stdout, stderr, returncode = execute_generated_file(backend_folder + "/code_writer_unit_test_usecase/function_AI_generated.py")
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
