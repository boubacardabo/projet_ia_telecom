import os
import sys
backend_folder = f"{os.getcwd()}\\backend"
if backend_folder not in sys.path:
    sys.path.append(backend_folder)

path_to_remove = f"{os.getcwd()}\\backend\\dataset"
if path_to_remove in sys.path:
    sys.path.remove(path_to_remove)


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
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from embedding.model_names import all_MiniLM_L6_v2

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
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





