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
        from dataset import dataset
        from utils.main import write_function_to_file2


        id = 8
        function_string_whole = dataset[id][ 'whole_func_string']
        func_code_url = dataset[id]["func_code_url"]

        # write_function_to_file2(function_string_whole, backend_folder + "\\code_writer_usecase_dataset\\functions.py")


        os.environ["TAVILY_API_KEY"]= "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"
        from langchain_community.tools.tavily_search import TavilySearchResults
        search = TavilySearchResults()


        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_community.document_loaders import WebBaseLoader
        from langchain_community.vectorstores import FAISS
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from embedding.model_names import all_MiniLM_L6_v2

        loader = WebBaseLoader(func_code_url)
        docs = loader.load()
        documents = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        ).split_documents(docs)


        model_name = all_MiniLM_L6_v2


        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            encode_kwargs={"normalize_embeddings": True},
            model_kwargs={"device": "cuda"},
                    )
        vector = FAISS.from_documents(documents, embeddings)
        retriever = vector.as_retriever()


        from langchain.tools.retriever import create_retriever_tool

        retriever_tool = create_retriever_tool(
            retriever,
            "langsmith_search",
            "Search for information about a function.",
        )

        tools = [search, retriever_tool]

        from langchain import hub

        # Get the prompt to use - you can modify this!
        prompt = hub.pull("hwchase17/openai-functions-agent")
        from langchain.agents import create_openai_functions_agent

        agent = create_openai_functions_agent(llm, tools, prompt)

        from langchain.agents import AgentExecutor

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        print(agent_executor.invoke({"input": "What are the modules and function depending of face_locations?"}))



        ####



        langchain_wrapper.cleanup()

    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    main()
