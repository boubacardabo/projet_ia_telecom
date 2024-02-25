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
    os.environ["TAVILY_API_KEY"]= os.getenv("TAVILY_API_KEY")

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

            model = LlmModel(llm_runnable=True)


        else:
            print("Invalid choice. Exiting.")
            return
    


        # langchain
        langchain_wrapper = LangWrapper(model=model)
        langchain_wrapper.add_rag_wrapper(ragWrapper)
        langchain_wrapper.setup_rag_llm_chain()

        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_community.document_loaders import WebBaseLoader
        from langchain_community.vectorstores import Chroma
        from langchain_community.embeddings import GPT4AllEmbeddings
        from langchain_community.embeddings import LlamaCppEmbeddings
        from embedding.model_names import sentence_t5_base, codet5_base, all_MiniLM_L6_v2
        model_name = all_MiniLM_L6_v2
        # Load
        url = "https://lilianweng.github.io/posts/2023-06-23-agent/"
        loader = WebBaseLoader(url)
        docs = loader.load()

        # Split
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=500, chunk_overlap=100
        )
        all_splits = text_splitter.split_documents(docs)
        from langchain_community.embeddings import HuggingFaceEmbeddings
        # Embed and index
        embedding = HuggingFaceEmbeddings(
                    model_name=model_name,
                    encode_kwargs={"normalize_embeddings": True},
                    model_kwargs={"device": "cuda"},
                )
        # Index
        vectorstore = Chroma.from_documents(
            documents=all_splits,
            collection_name="rag-chroma",
            embedding=embedding,
        )
        retriever = vectorstore.as_retriever()

        from typing import Annotated, Dict, TypedDict

        from langchain_core.messages import BaseMessage


        class GraphState(TypedDict):
            """
            Represents the state of our graph.

            Attributes:
                keys: A dictionary where each key is a string.
            """

            keys: Dict[str, any]



        import json
        import operator
        from typing import Annotated, Sequence, TypedDict

        from langchain import hub
        from langchain_core.output_parsers import JsonOutputParser
        from langchain.prompts import PromptTemplate
        from langchain.schema import Document
        from langchain_community.chat_models import ChatOllama
        from langchain_community.tools.tavily_search import TavilySearchResults
        from langchain_community.vectorstores import Chroma
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.runnables import RunnablePassthrough


        ### Nodes ###


        def retrieve(state):
            """
            Retrieve documents

            Args:
                state (dict): The current graph state

            Returns:
                state (dict): New key added to state, documents, that contains retrieved documents
            """
            print("---RETRIEVE---")
            state_dict = state["keys"]
            question = state_dict["question"]
            local = state_dict["local"]
            documents = retriever.get_relevant_documents(question)
            return {"keys": {"documents": documents, "local": local, "question": question}}


        def generate(state):
            """
            Generate answer

            Args:
                state (dict): The current graph state

            Returns:
                state (dict): New key added to state, generation, that contains generation
            """
            print("---GENERATE---")
            state_dict = state["keys"]
            question = state_dict["question"]
            documents = state_dict["documents"]
            local = state_dict["local"]

            # Prompt
            prompt = hub.pull("rlm/rag-prompt")

            llm = model.llm

            # Post-processing
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            # Chain
            rag_chain = prompt | llm | StrOutputParser()

            # Run
            generation = rag_chain.invoke({"context": documents, "question": question})
            return {
                "keys": {"documents": documents, "question": question, "generation": generation}
            }


        def grade_documents(state):
            """
            Determines whether the retrieved documents are relevant to the question.

            Args:
                state (dict): The current graph state

            Returns:
                state (dict): Updates documents key with relevant documents
            """

            print("---CHECK RELEVANCE---")
            state_dict = state["keys"]
            question = state_dict["question"]
            documents = state_dict["documents"]
            local = state_dict["local"]

            llm = model.llm

            prompt = PromptTemplate(
                template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
                Here is the retrieved document: \n\n {context} \n\n
                Here is the user question: {question} \n
                If the document contains keywords related to the user question, grade it as relevant. \n
                It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
                Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
                Provide the binary score as a JSON with a single key 'score' and no premable or explaination.""",
                input_variables=["question", "context"],
            )

            chain = prompt | llm | JsonOutputParser()

            # Score
            filtered_docs = []
            search = "No"  # Default do not opt for web search to supplement retrieval
            for d in documents:
                score = chain.invoke(
                    {
                        "question": question,
                        "context": d.page_content,
                    }
                )
                grade = score["score"]
                if grade == "yes":
                    print("---GRADE: DOCUMENT RELEVANT---")
                    filtered_docs.append(d)
                else:
                    print("---GRADE: DOCUMENT NOT RELEVANT---")
                    search = "Yes"  # Perform web search
                    continue

            return {
                "keys": {
                    "documents": filtered_docs,
                    "question": question,
                    "local": local,
                    "run_web_search": search,
                }
            }


        def transform_query(state):
            """
            Transform the query to produce a better question.

            Args:
                state (dict): The current graph state

            Returns:
                state (dict): Updates question key with a re-phrased question
            """

            print("---TRANSFORM QUERY---")
            state_dict = state["keys"]
            question = state_dict["question"]
            documents = state_dict["documents"]
            local = state_dict["local"]

            # Create a prompt template with format instructions and the query
            prompt = PromptTemplate(
                template="""You are generating questions that is well optimized for retrieval. \n 
                Look at the input and try to reason about the underlying sematic intent / meaning. \n 
                Here is the initial question:
                \n ------- \n
                {question} 
                \n ------- \n
                Provide an improved question without any premable, only respond with the updated question: """,
                input_variables=["question"],
            )

            # Grader
            # LLM
            llm = model.llm

            # Prompt
            chain = prompt | llm | StrOutputParser()
            better_question = chain.invoke({"question": question})

            return {
                "keys": {"documents": documents, "question": better_question, "local": local}
            }


        def web_search(state):
            """
            Web search based on the re-phrased question using Tavily API.

            Args:
                state (dict): The current graph state

            Returns:
                state (dict): Web results appended to documents.
            """

            print("---WEB SEARCH---")
            state_dict = state["keys"]
            question = state_dict["question"]
            documents = state_dict["documents"]
            local = state_dict["local"]

            tool = TavilySearchResults()
            docs = tool.invoke({"query": question})
            web_results = "\n".join([d["content"] for d in docs])
            web_results = Document(page_content=web_results)
            documents.append(web_results)

            return {"keys": {"documents": documents, "local": local, "question": question}}


        ### Edges


        def decide_to_generate(state):
            """
            Determines whether to generate an answer or re-generate a question for web search.

            Args:
                state (dict): The current state of the agent, including all keys.

            Returns:
                str: Next node to call
            """

            print("---DECIDE TO GENERATE---")
            state_dict = state["keys"]
            question = state_dict["question"]
            filtered_documents = state_dict["documents"]
            search = state_dict["run_web_search"]

            if search == "Yes":
                # All documents have been filtered check_relevance
                # We will re-generate a new query
                print("---DECISION: TRANSFORM QUERY and RUN WEB SEARCH---")
                return "transform_query"
            else:
                # We have relevant documents, so generate answer
                print("---DECISION: GENERATE---")
                return "generate"



        import pprint

        from langgraph.graph import END, StateGraph

        workflow = StateGraph(GraphState)

        # Define the nodes
        workflow.add_node("retrieve", retrieve)  # retrieve
        workflow.add_node("grade_documents", grade_documents)  # grade documents
        workflow.add_node("generate", generate)  # generatae
        workflow.add_node("transform_query", transform_query)  # transform_query
        workflow.add_node("web_search", web_search)  # web search

        # Build graph
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "grade_documents")
        workflow.add_conditional_edges(
            "grade_documents",
            decide_to_generate,
            {
                "transform_query": "transform_query",
                "generate": "generate",
            },
        )
        workflow.add_edge("transform_query", "web_search")
        workflow.add_edge("web_search", "generate")
        workflow.add_edge("generate", END)

        # Compile
        app = workflow.compile()
        
        run_local = "Yes"

        # Run
        inputs = {
            "keys": {
                "question": "Explain how the different types of agent memory work?",
                "local": run_local,
            }
        }
        for output in app.stream(inputs):
            for key, value in output.items():
                # Node
                pprint.pprint(f"Node '{key}':")
                # Optional: print full state at each node
                # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
            pprint.pprint("\n---\n")

        # Final generation
        pprint.pprint(value["keys"]["generation"])



        langchain_wrapper.cleanup()
    
    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    main()
