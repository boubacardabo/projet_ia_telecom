import os
import sys

backend_folder = f"{os.getcwd()}/backend"
sys.path.append(backend_folder)

os.environ["LANGCHAIN_TRACING_V2"] = 'true'
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__a21c5d9069a442c08645e82f0a7330cc"
os.environ["LANGCHAIN_PROJECT"]= "PRIM-NXP"

from embedding.rag_wrapper import RagWrapper
from langchain_wrapper.lang_wrapper import LangWrapper




def main():
    try:


        # rag
        repo_url = ""
        branch = "dev"
        file_type = ".py"
        ragWrapper = RagWrapper(repo_url=repo_url, branch=branch, file_type=file_type)




        choice = input("Choose HuggingFaceAPI ('h') or OpenLLM ('o'):\n ").lower().strip()
        if choice == 'h':

            print("You are using the huggingFace pipeline API.\n")

            
        elif choice == 'o':

            print("You are using OpenLLM.\n")


            from langchain_community.llms import OpenLLM

            server_url = "http://localhost:3000"
            llm = OpenLLM(server_url=server_url)

            langchain_wrapper = LangWrapper(model=llm)
            langchain_wrapper.add_rag_wrapper(ragWrapper)
            langchain_wrapper.setup_rag_llm_chain()

            while True:
                question = input("Ask a query (type 'q' to quit): \n").strip()
                if question.lower() == 'q':
                    break
                
                generated_text = langchain_wrapper.invoke_llm_chain(question)
                print(generated_text['answer'])



        else:
            print("Invalid choice. Exiting.")
            return
    
        langchain_wrapper.cleanup()
            

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
