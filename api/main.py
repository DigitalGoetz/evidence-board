from fastapi import FastAPI
from graph import GraphClient
import uvicorn

app = FastAPI()
graph_client = GraphClient()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/evidence")
async def get_evidence():
    return graph_client.get_entries()

@app.post("/evidence")
async def create_evidence(title: str, description: str):
    graph_client.create_entry(title, description)
    return {"message": "Evidence created successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)