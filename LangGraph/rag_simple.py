from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END


# ============================================================
# ENUNCIADO : LangGraph Ejemplo 4 — RAG simple con recuperación semántica
# DESCRIPCIÓN: Implementa un flujo Retrieve-Augment-Generate donde el grafo
#              recupera documentos relevantes, valida si hay contexto suficiente
#              y enruta la respuesta: contestar con la documentación encontrada
#              o solicitar más información al usuario.
#
# CASO DE USO : Asistente de documentación técnica del BFF que responde preguntas
#               sobre eventos SSE (act, action, diagnostic, heartbeat, sse_error)
#               consultando la base de conocimiento interna.
#
# CATEGORÍA DE NEGOCIO: Soporte técnico / Gestión del conocimiento
#
# OTROS EJEMPLOS:
#   1. Responder preguntas de clientes sobre productos bancarios usando documentos PDF.
#   2. Asistente interno que consulta manuales de operaciones antes de responder.
#   3. Bot de onboarding que busca en FAQs y escala si no hay respuesta suficiente.
# ============================================================

class RagState(TypedDict):
    question: str
    docs: List[str]
    has_context: bool
    answer: str

def retrieve_docs(state: RagState) -> RagState:
    fake_docs = [
        "Los eventos SSE soportados son act, action, diagnostic, heartbeat y sse_error."
    ]

    question = state["question"].lower()

    if "sse" in question:
        docs = fake_docs
    else:
        docs = []

    return {
        **state,
        "docs": docs
    }

def validate_context(state: RagState) -> RagState:
    return {
        **state,
        "has_context": len(state["docs"]) > 0
    }

def answer_with_context(state: RagState) -> RagState:
    context = "\n".join(state["docs"])

    return {
        **state,
        "answer": f"Según la documentación encontrada: {context}"
    }

def ask_for_more_info(state: RagState) -> RagState:
    return {
        **state,
        "answer": "No encontré suficiente contexto. ¿Puedes especificar el módulo o endpoint?"
    }

def route_by_context(state: RagState) -> str:
    if state["has_context"]:
        return "answer_with_context"
    return "ask_for_more_info"

graph = StateGraph(RagState)

graph.add_node("retrieve_docs", retrieve_docs)
graph.add_node("validate_context", validate_context)
graph.add_node("answer_with_context", answer_with_context)
graph.add_node("ask_for_more_info", ask_for_more_info)

graph.add_edge(START, "retrieve_docs")
graph.add_edge("retrieve_docs", "validate_context")

graph.add_conditional_edges(
    "validate_context",
    route_by_context,
    {
        "answer_with_context": "answer_with_context",
        "ask_for_more_info": "ask_for_more_info"
    }
)


graph.add_edge("answer_with_context", END)
graph.add_edge("ask_for_more_info", END)

app = graph.compile()

result = app.invoke({
    "question": "¿Qué eventos sse soporta el BFF?",
    "docs": [],
    "has_context": False,
    "answer": ""
})

print(result["answer"])