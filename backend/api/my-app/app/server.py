from fastapi import FastAPI
from langserve import add_routes

import sys
import os

def get_first_three_folders_path(cwd):
    folders = cwd.split(os.path.sep)
    first_three_folders_path = os.path.sep.join(folders[:4])
    return first_three_folders_path

cwd = os.getcwd()
first_three_folders_path = get_first_three_folders_path(cwd)

sys.path.append(first_three_folders_path)
sys.path.append(first_three_folders_path + "/backend")


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="API server using Langchain's Runnable interfaces",
)




from packages.llm_chain import chain as llm


add_routes(
    app,
    llm,
    path="/llm",
)

# from packages.rag_chain import chain as ragChain


# add_routes(
#     app,
#     ragChain,
#     path="/rag-chain",
# )



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)