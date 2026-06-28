from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ============================================================
# ENUNCIADO : LangGraph Ejemplo 3 — Human-in-the-loop (revisión humana)
# DESCRIPCIÓN: Pausa el flujo del grafo para que un humano revise y apruebe
#              un borrador antes de continuar. El nodo human_review solicita
#              input por terminal con True como valor por defecto.
#
# CASO DE USO : Flujo de comunicación al equipo técnico donde el LLM genera
#               la respuesta pero un supervisor debe aprobarla antes de que
#               se envíe, evitando mensajes incorrectos o incompletos.
#
# CATEGORÍA DE NEGOCIO: Gobernanza de IA / Operaciones críticas
#
# OTROS EJEMPLOS:
#   1. Aprobar transferencias bancarias de alto monto generadas por un agente automatizado.
#   2. Revisar respuestas automáticas a clientes antes de enviarlas desde el CRM.
#   3. Validar cambios de configuración en producción propuestos por un agente de DevOps.
# ============================================================

class ReviewState(TypedDict):
    user_request: str
    draft_response: str
    approved: bool
    final_response: str


def generate_draft(state: ReviewState) -> ReviewState:
    draft = f"""
    Propuesta de respuesta:

    Hola equipo, se identificó el problema reportado.
    Vamos a validar el flujo, revisar logs y confirmar el resultado.
    """
    return {
        **state,
        "draft_response": draft
    }

def human_review(state: ReviewState) -> ReviewState:
    print("\n--- REVISIÓN HUMANA ---")
    print(state["draft_response"])
    raw = input("¿Aprobar respuesta? [True/False] (default: True): ").strip().lower()
    if raw == "false":
        approved = False
    else:
        approved = True
    return {
        **state,
        "approved": approved
    }

def send_response(state: ReviewState) -> ReviewState:
    if state["approved"]:
        final_response = state["draft_response"]
    else:
        final_response = "La respuesta necesita ajustes antes de enviarse."

    return {
        **state,
        "final_response": final_response
    }

graph = StateGraph(ReviewState)

graph.add_node("generate_draft", generate_draft)
graph.add_node("human_review", human_review)
graph.add_node("send_response", send_response)

graph.add_edge(START, "generate_draft")
graph.add_edge("generate_draft", "human_review")
graph.add_edge("human_review", "send_response")
graph.add_edge("send_response", END)

app = graph.compile()

response = app.invoke({
    "user_request": "Preparar mensaje para el equipo técnico.",
    "draft_response": "",
    "approved": False,
    "final_response": ""
})

print(response["final_response"])