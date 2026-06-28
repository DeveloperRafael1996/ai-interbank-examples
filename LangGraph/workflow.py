from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ============================================================
# ENUNCIADO : LangGraph Ejemplo 1 — Workflow simple con estado compartido
# DESCRIPCIÓN: Define un grafo lineal con dos nodos (normalize → classify) que
#              comparten un estado TypedDict. Cada nodo recibe el estado completo,
#              lo enriquece y lo pasa al siguiente sin perder información previa.
#
# CASO DE USO : Pipeline de validación de mensajes entrantes en un sistema de
#               eventos SSE: normalizar el texto del evento y detectar si contiene
#               errores antes de procesarlo.
#
# CATEGORÍA DE NEGOCIO: Procesamiento de eventos / Calidad de datos
#
# OTROS EJEMPLOS:
#   1. Normalizar y validar payloads JSON recibidos de webhooks externos.
#   2. Preprocesar texto de tickets de soporte antes de enviarlo al clasificador.
#   3. Limpiar y estandarizar datos de formularios antes de guardarlos en base de datos.
# ============================================================

class WorkflowState(TypedDict):
    input: str
    normalized_text: str
    result: str

def normalize_text(state: WorkflowState) -> WorkflowState:
    text = state["input"].strip().lower()
    return {
        **state,
        "normalized_text": text
    }

def classify_text(state: WorkflowState) -> WorkflowState:
    text = state["normalized_text"]

    if "error" in text or "failed" in text:
        result = "ERROR_DETECTED"
    else:
        result = "OK"

    return {
        **state,
        "result": result
    }

graph = StateGraph(WorkflowState)

graph.add_node("normalize_text", normalize_text)
graph.add_node("classify_text", classify_text)


graph.add_edge(START, "normalize_text")
graph.add_edge("normalize_text", "classify_text")
graph.add_edge("classify_text", END)

app = graph.compile()

response = app.invoke({
    "input": "the operation succeeded",
    "normalized_text": "",
    "result": ""
})

print(response)