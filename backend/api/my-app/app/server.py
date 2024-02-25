from fastapi import FastAPI
from langserve import add_routes

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)


server_url = "http://localhost:3000"
from langchain_community.llms import OpenLLM
llm = OpenLLM(server_url=server_url)


add_routes(
    app,
    llm,
    path="/test",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)