import os
import sys
import argparse


backend_folder = f"{os.path.expanduser('~')}/projet_ia_telecom/backend"
sys.path.append(backend_folder)

from fastapi import FastAPI, Response, Body
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

args = parser.parse_args()

apiservice = ApiService(
    LlmModel(model_name=args.model_name, is_open_llm=args.is_open_llm)
)


@app.get("/")
async def root():
    # Customize the response message as needed
    return Response("FastAPI app is running!")


@app.post("/setup_use_case/")
async def setup_use_case(data=Body(...)):
    print(data)
    return apiservice.create_use_case_session(**data)


@app.post("/invoke_use_case/")
async def invoke_use_case(data: dict = Body(...)):
    return apiservice.invoke_use_case(**data)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=7000)
