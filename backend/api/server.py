
#!/usr/bin/env python
"""A server for the chain above."""
import os
import sys

backend_folder = f"{os.getcwd()}/backend"
sys.path.append(backend_folder)


from fastapi import FastAPI
from langserve import add_routes
from test.main import chain

app = FastAPI(title="Retrieval App")

add_routes(app, chain)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)