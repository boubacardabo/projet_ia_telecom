import os
import sys

backend_folder = f"{os.getcwd()}/backend"
if backend_folder not in sys.path:
    sys.path.append(backend_folder)

path_to_remove = f"{os.getcwd()}/backend/code_writer_usecase_dataset"
if path_to_remove in sys.path:
    sys.path.remove(path_to_remove)


import traceback

os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__a21c5d9069a442c08645e82f0a7330cc"
os.environ["LANGCHAIN_PROJECT"]= "PRIM-NXP"
os.environ["TAVILY_API_KEY"]= "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"

from embedding.rag_wrapper import RagWrapper
from langchain_wrapper.lang_wrapper import LangWrapper




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

            langchain_wrapper = LangWrapper(model=llm)
            langchain_wrapper.add_rag_wrapper(ragWrapper)
            langchain_wrapper.setup_rag_llm_chain()


        else:
            print("Invalid choice. Exiting.")
            return
    


        ####
        

        from langchain.tools.retriever import create_retriever_tool
        from langchain import hub
        from langchain.agents import AgentExecutor, create_react_agent

        retriever = langchain_wrapper.ragWrapper.retriever

        retriever_tool = create_retriever_tool(
            retriever,
            "RAG-search",
            "This is a RAG tool to search relevant information about the class before writing a system test for it."
        )



        tools = [retriever_tool]

        # Get the prompt to use
        prompt = hub.pull("parrottheparrot/prim-test-react")

        # Construct the ReAct agent
        agent = create_react_agent(llm, tools, prompt)

        # Create an agent executor by passing in the agent and tools
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        #Run agent
        input_query = "class PinRegistry"
        print(f"input : {input_query}\n")
        generated_output = agent_executor.invoke({"input": input_query})
        print(generated_output["output"])



        print("\n --------------------------------------- \n")

        from utils.main import extract_function_from_markdown2, write_function_to_file2, execute_generated_file
       
        #extract the Python code out of the output
        function_code = extract_function_from_markdown2(generated_output["output"])


        #Write the function in the file function_AI_generated.py, containing import and PyTest launch
        if function_code: #if a some code has been found

            write_function_to_file2(function_code, backend_folder + "/code_writer_usecase_dataset/function_AI_generated.py", backend_folder=backend_folder)
            print("Function code has been written to 'function_AI_generated.py'")
        else:
            print("No function code extracted from the Markdown string.")

    
        #file execution
        stdout, stderr, returncode = execute_generated_file(backend_folder + "/code_writer_usecase_dataset/function_AI_generated.py")
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
