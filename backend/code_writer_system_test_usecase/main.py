import os
import sys
import traceback
from dotenv import load_dotenv


backend_folder = f"{os.getcwd()}/backend"
if backend_folder not in sys.path:
    sys.path.append(backend_folder)

path_to_remove = f"{os.getcwd()}/backend/code_writer_system_test_usecase"
if path_to_remove in sys.path:
    sys.path.remove(path_to_remove)




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


            
        elif choice == 'o':

            print("You are using OpenLLM.\n")


            model = LlmModel(llm_runnable=True)



        else:
            print("Invalid choice. Exiting.")
            return
    

        langchain_wrapper = LangWrapper(model=model)
        langchain_wrapper.add_rag_wrapper(ragWrapper)
        langchain_wrapper.setup_rag_llm_chain()

        ####

        # Get the path of the currently executing script
        script_path = os.path.abspath(__file__)

        # Split the script directory path into its components
        directory_components = script_path.split(os.path.sep)

        # Join the first three components back together (Télécom GPU : /home/infres/<name>)
        parent_directories = os.path.sep.join(directory_components[:4])



        from langchain.tools.retriever import create_retriever_tool
        from langchain.agents import AgentExecutor, create_react_agent
        from prompt.prompts import prompt_usecase_test_system

        retriever = langchain_wrapper.ragWrapper.retriever

        retriever_tool = create_retriever_tool(
            retriever,
            "RAG-search",
            "This is a RAG tool to search relevant information about the object before writing a system test for it. To use it, It should take in input keywords such as name of files, name of functions, name of classes, each separated with blank spaces."
        )



        tools = [retriever_tool]

        # Get the prompt to use
        prompt = prompt_usecase_test_system

        # Construct the ReAct agent
        agent = create_react_agent(model.llm, tools, prompt)

        # Create an agent executor by passing in the agent and tools
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        #Run agent
        input_query = "method iter_component_configs at config.py"
        print(f"input : {input_query}\n")
        generated_output = agent_executor.invoke({"input": input_query})
        print(generated_output["output"])



        print("\n --------------------------------------- \n")

        from utils.utils import extract_function_from_markdown, write_function_to_file2, execute_generated_file
       
        #extract the Python code out of the output
        function_code = extract_function_from_markdown(generated_output["output"], remove_imports=False)


        #Write the function in the file function_AI_generated.py, containing import and PyTest launch
        if function_code: #if a some code has been found

            write_function_to_file2(function_code, parent_directories + "/remote_code/esphome/function_AI_generated.py", backend_folder=backend_folder)
            #write_function_to_file2(function_code, backend_folder + "/code_writer_system_test_usecase/function_AI_generated.py", backend_folder=backend_folder)
            print("Function code has been written to 'function_AI_generated.py'")
        else:
            print("No function code extracted from the Markdown string.")

    
        #file execution
        # stdout, stderr, returncode = execute_generated_file(backend_folder + "/code_writer_system_test_usecase/function_AI_generated.py")
        stdout, stderr, returncode = execute_generated_file(parent_directories + "/remote_code/esphome/function_AI_generated.py")
        print("Standard output:")
        print(stdout)
        print("Standard error:")
        print(stderr)
        print("Return code:")
        print(returncode)

        ####



        langchain_wrapper.cleanup()

    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    main()
