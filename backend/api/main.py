import os
import sys

backend_folder = f"{os.path.expanduser('~')}/projet_ia_telecom/backend"
sys.path.append(backend_folder)

from fastapi import FastAPI, Response
from llm.llm_model import LlmModel
from llm.model_names import mistral_model
import uvicorn


app = FastAPI()
LlmModel(model_name=mistral_model)


@app.get("/")
async def root():
    # Customize the response message as needed
    return Response("FastAPI app is running!")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=7000)
