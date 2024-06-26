import os
import sys
import argparse
import json
import signal


backend_folder = f"{os.path.expanduser('~')}/projet_ia_telecom/backend"
sys.path.append(backend_folder)

from fastapi import FastAPI, Response, Request
from llm.llm_model import LlmModel
from llm.model_names import mistral_model
from api_service import ApiService
import uvicorn


app = FastAPI()
parser = argparse.ArgumentParser(description="FastAPI app")
parser.add_argument(
    "--model_name", type=str, default=mistral_model, help="Name of the model to use"
)
parser.add_argument("--is_open_llm", type=bool, default=False, help="OpenLLM used")

parser.add_argument(
    "--langchain_api_key", type=str, default="", help="LangChain API key"
)

args = parser.parse_args()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "PRIM-NXP"
os.environ["LANGCHAIN_API_KEY"] = args.langchain_api_key

apiservice = ApiService(
    LlmModel(model_name=args.model_name, is_open_llm=args.is_open_llm)
)


@app.get("/")
async def root():
    # Customize the response message as needed
    return Response("FastAPI app is running!")


@app.post("/setup_use_case/")
async def setup_use_case(request: Request):
    body = await request.body()
    body_data = json.loads(body)
    kwargs = body_data

    return apiservice.create_use_case_session(**kwargs)


@app.post("/invoke_use_case/")
async def invoke_use_case(request: Request):
    body = await request.body()
    body_data = json.loads(body)
    kwargs = body_data

    return apiservice.invoke_use_case(**kwargs)


def signal_handler(sig, frame):
    apiservice.llm_model.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=7000)
