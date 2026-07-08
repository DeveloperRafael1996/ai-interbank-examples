from fastapi import FastAPI
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI

app = FastAPI()

documents = SimpleDirectoryReader("./docs/productos_banco").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(llm=OpenAI(model="gpt-4o-mini"))


class AgentMessage(BaseModel):
    task_id: str
    message: str
    sender: str


@app.get("/agent-card")
def get_agent_card():
    return {
        "name": "ProductRAGAgent",
        "description": "Agente especializado en productos bancarios",
        "skills": [
            "consultar_productos",
            "responder_politicas",
            "resumir_documentos"
        ],
        "input_modes": ["text"],
        "output_modes": ["text"]
    }


@app.post("/tasks")
def execute_task(payload: AgentMessage):
    response = query_engine.query(payload.message)

    return {
        "task_id": payload.task_id,
        "agent": "ProductRAGAgent",
        "status": "completed",
        "response": str(response)
    }